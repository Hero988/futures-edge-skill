#!/usr/bin/env python3
"""
prop_firm_check.py - Validate trade / EOD against prop firm rules.
Args: --firm, --account-size, --pnl, --trades, --time, --position-size,
      --eod, --daily-pnl, --total-profit, --high-water-mark, --drawdown-floor.
Reads prop-firm-profiles.json from ../assets/.
Outputs JSON compliance report to stdout.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_prop_firm_profiles():
    """Load prop firm profiles from assets directory."""
    profiles_path = Path(__file__).resolve().parent.parent / "assets" / "prop-firm-profiles.json"
    try:
        with open(profiles_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        return {"_error": f"Invalid JSON in prop-firm-profiles.json: {e}"}


def resolve_nested_value(value, plan=None):
    """Resolve a value that may be a dict (plan-specific like MFFU) or a simple value."""
    if isinstance(value, dict) and plan:
        return value.get(plan, value.get(list(value.keys())[0]) if value else None)
    if isinstance(value, dict) and not plan:
        # Return the first available value, or None
        for v in value.values():
            if v is not None:
                return v
        return None
    return value


def get_account_rules(firm_data, account_size_str, plan=None):
    """Extract rules for a given account size."""
    accounts = firm_data.get("accounts", {})

    # Try direct match
    if account_size_str in accounts:
        acct = accounts[account_size_str]
    else:
        # Try matching by numeric value (e.g., 50000 -> "50k")
        try:
            size_k = str(int(int(account_size_str) / 1000)) + "k"
            acct = accounts.get(size_k, {})
        except (ValueError, TypeError):
            return None

    if not acct:
        return None

    rules = {
        "profit_target": resolve_nested_value(acct.get("profit_target"), plan),
        "max_drawdown": resolve_nested_value(acct.get("max_drawdown"), plan),
        "daily_loss_limit": resolve_nested_value(acct.get("daily_loss_limit"), plan),
        "max_contracts": resolve_nested_value(acct.get("max_contracts"), plan),
        "max_micros": resolve_nested_value(acct.get("max_micros"), plan),
    }
    return rules


def parse_close_time(close_by_str):
    """Parse firm close_by time string into a datetime.time object."""
    if not close_by_str:
        return None, None

    # Normalize timezone labels
    tz_map = {"CT": "CT", "CST": "CT", "CDT": "CT", "ET": "ET", "EST": "ET", "EDT": "ET"}

    parts = close_by_str.strip().split()
    if len(parts) < 2:
        return None, None

    time_str = parts[0]
    tz_label = parts[1] if len(parts) > 1 else "CT"
    norm_tz = tz_map.get(tz_label, tz_label)

    try:
        t = datetime.strptime(time_str, "%H:%M").time()
        return t, norm_tz
    except ValueError:
        return None, None


def check_time_compliance(current_time_str, close_by_str):
    """Check if current time is within trading hours or near close deadline."""
    close_time, tz = parse_close_time(close_by_str)
    if close_time is None:
        return {"compliant": True, "warning": None, "must_close_by": close_by_str}

    try:
        if current_time_str.lower() == "now":
            current = datetime.now().time()
        else:
            current = datetime.strptime(current_time_str, "%H:%M").time()
    except ValueError:
        return {"compliant": True, "warning": "Could not parse current time", "must_close_by": close_by_str}

    # Convert to minutes for comparison
    current_minutes = current.hour * 60 + current.minute
    close_minutes = close_time.hour * 60 + close_time.minute

    minutes_until_close = close_minutes - current_minutes

    result = {
        "compliant": True,
        "warning": None,
        "must_close_by": close_by_str,
        "minutes_until_close": minutes_until_close,
    }

    if minutes_until_close <= 0:
        result["compliant"] = False
        result["warning"] = f"PAST CLOSE DEADLINE: All positions must be closed by {close_by_str}"
    elif minutes_until_close <= 15:
        result["warning"] = f"URGENT: Only {minutes_until_close} minutes until close deadline ({close_by_str})"
    elif minutes_until_close <= 30:
        result["warning"] = f"CAUTION: {minutes_until_close} minutes until close deadline ({close_by_str})"

    return result


def check_consistency(daily_pnl, total_profit, consistency_rule, is_eval=False):
    """Check consistency rule compliance."""
    result = {
        "status": "ok",
        "current_pct": None,
        "limit_pct": None,
        "compliant": True,
        "warning": None,
    }

    if not consistency_rule:
        result["status"] = "no_rule"
        return result

    # Determine which rule applies
    if is_eval:
        limit = consistency_rule.get("eval")
    else:
        limit = consistency_rule.get("funded")

    # Handle nested funded rules (e.g., MFFU per-plan)
    if isinstance(limit, dict):
        # Take the most restrictive non-null value
        limits = [v for v in limit.values() if v is not None]
        limit = min(limits) if limits else None

    if limit is None:
        result["status"] = "no_rule"
        return result

    if total_profit is None or total_profit <= 0:
        result["status"] = "insufficient_data"
        result["warning"] = "Total profit <= 0 or not provided; consistency rule cannot be evaluated."
        return result

    if daily_pnl is not None:
        current_pct = daily_pnl / total_profit if total_profit > 0 else 0
        result["current_pct"] = round(current_pct * 100, 2)
        result["limit_pct"] = round(limit * 100, 2)

        if current_pct > limit:
            result["compliant"] = False
            result["status"] = "violation"
            result["warning"] = (
                f"Consistency violation: today's P&L (${daily_pnl}) is "
                f"{result['current_pct']}% of total profit (${total_profit}), "
                f"exceeding the {result['limit_pct']}% limit."
            )
        elif current_pct > limit * 0.75:
            result["status"] = "warning"
            result["warning"] = (
                f"Approaching consistency limit: today's P&L is "
                f"{result['current_pct']}% of total profit "
                f"(limit: {result['limit_pct']}%)."
            )
    else:
        result["status"] = "insufficient_data"

    return result


def main():
    parser = argparse.ArgumentParser(description="Prop firm compliance checker")
    parser.add_argument("--firm", required=True, help="Firm name (topstep, apex, bulenox, mffu, tradeday)")
    parser.add_argument("--account-size", type=str, default=None, help="Account size (e.g., 50000 or 50k)")
    parser.add_argument("--pnl", type=float, default=None, help="Today's current P&L ($)")
    parser.add_argument("--trades", type=int, default=None, help="Number of trades today")
    parser.add_argument("--time", default="now", help="Current time HH:MM or 'now'")
    parser.add_argument("--position-size", type=int, default=None, help="Proposed position size (contracts)")
    parser.add_argument("--eod", action="store_true", help="End-of-day check mode")
    parser.add_argument("--daily-pnl", type=float, default=None, help="Today's final P&L (for consistency)")
    parser.add_argument("--total-profit", type=float, default=None, help="Total account profit to date")
    parser.add_argument("--high-water-mark", type=float, default=None, help="Account high water mark")
    parser.add_argument("--drawdown-floor", type=float, default=None, help="Current drawdown floor")
    parser.add_argument("--plan", default=None, help="Firm plan (e.g., core/rapid/pro for MFFU)")
    parser.add_argument("--is-eval", action="store_true", help="Whether this is evaluation (not funded)")
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "firm": args.firm,
        "account_size": args.account_size,
        "mode": "eod" if args.eod else "pre_trade",
        "compliant": True,
        "warnings": [],
        "violations": [],
        "remaining_daily_loss": None,
        "must_close_by": None,
        "max_contracts": None,
        "consistency": None,
        "drawdown": None,
        "error": None,
    }

    # Load profiles
    profiles = load_prop_firm_profiles()
    if profiles is None:
        output["error"] = "prop-firm-profiles.json not found in assets directory."
        output["compliant"] = False
        print(json.dumps(output, indent=2))
        return
    if "_error" in profiles:
        output["error"] = profiles["_error"]
        output["compliant"] = False
        print(json.dumps(output, indent=2))
        return

    # Find firm
    firm_key = args.firm.lower().replace(" ", "").replace("-", "")
    firm_data = profiles.get(firm_key)
    if not firm_data:
        # Try partial match
        for key, data in profiles.items():
            if key.startswith("_"):
                continue
            if firm_key in key.lower() or firm_key in data.get("name", "").lower().replace(" ", ""):
                firm_data = data
                firm_key = key
                break

    if not firm_data:
        output["error"] = f"Firm '{args.firm}' not found in profiles. Available: {[k for k in profiles.keys() if not k.startswith('_')]}"
        output["compliant"] = False
        print(json.dumps(output, indent=2))
        return

    output["firm"] = firm_data.get("name", args.firm)

    # Resolve account size
    acct_size = args.account_size
    if acct_size is None:
        # Default to first available account
        accounts = firm_data.get("accounts", {})
        if accounts:
            acct_size = list(accounts.keys())[0]
        else:
            output["error"] = "No account size provided and no accounts found in firm profile."
            output["compliant"] = False
            print(json.dumps(output, indent=2))
            return

    # Normalize account size
    if acct_size.isdigit():
        acct_size_key = str(int(int(acct_size) / 1000)) + "k"
    else:
        acct_size_key = acct_size.lower().replace("$", "").replace(",", "")

    rules = get_account_rules(firm_data, acct_size_key, args.plan)
    if rules is None:
        output["error"] = f"Account size '{acct_size}' not found for {firm_data.get('name')}. Available: {list(firm_data.get('accounts', {}).keys())}"
        output["compliant"] = False
        print(json.dumps(output, indent=2))
        return

    # --- CHECKS ---

    # 1. Daily loss limit
    daily_loss_limit = rules.get("daily_loss_limit")
    pnl = args.daily_pnl if args.daily_pnl is not None else args.pnl

    if daily_loss_limit is not None and pnl is not None:
        remaining = daily_loss_limit + pnl  # pnl is negative for losses
        output["remaining_daily_loss"] = round(remaining, 2)

        if pnl < 0 and abs(pnl) >= daily_loss_limit:
            output["violations"].append(
                f"DAILY LOSS LIMIT EXCEEDED: P&L ${pnl} exceeds daily limit of -${daily_loss_limit}"
            )
            output["compliant"] = False
        elif remaining < daily_loss_limit * 0.25:
            output["warnings"].append(
                f"Within 25% of daily loss limit: ${remaining:.2f} remaining (limit: ${daily_loss_limit})"
            )
    elif daily_loss_limit is None:
        output["remaining_daily_loss"] = None
        # Some firms (Apex, MFFU, TradeDay) don't have daily loss limits
    else:
        if daily_loss_limit is not None:
            output["remaining_daily_loss"] = daily_loss_limit

    # 2. Position size
    max_contracts = rules.get("max_contracts")
    output["max_contracts"] = max_contracts

    if args.position_size is not None and max_contracts is not None:
        if args.position_size > max_contracts:
            output["violations"].append(
                f"POSITION SIZE VIOLATION: {args.position_size} contracts exceeds max of {max_contracts}"
            )
            output["compliant"] = False
        elif args.position_size > max_contracts * 0.8:
            output["warnings"].append(
                f"Near max position size: {args.position_size}/{max_contracts} contracts"
            )

    # 3. Time / close deadline
    close_by = firm_data.get("close_by")
    output["must_close_by"] = close_by

    if close_by:
        time_check = check_time_compliance(args.time, close_by)
        if not time_check["compliant"]:
            output["violations"].append(time_check["warning"])
            output["compliant"] = False
        elif time_check.get("warning"):
            output["warnings"].append(time_check["warning"])

    # 4. Drawdown check
    max_drawdown = rules.get("max_drawdown")
    if isinstance(max_drawdown, dict):
        # Some firms have multiple drawdown types (e.g., TradeDay)
        dd_type = firm_data.get("drawdown_type", [])
        if isinstance(dd_type, list) and dd_type:
            max_drawdown = max_drawdown.get(dd_type[0], list(max_drawdown.values())[0])
        else:
            max_drawdown = list(max_drawdown.values())[0]

    drawdown_info = {
        "max_drawdown": max_drawdown,
        "drawdown_type": firm_data.get("drawdown_type"),
        "high_water_mark": args.high_water_mark,
        "drawdown_floor": args.drawdown_floor,
        "remaining": None,
    }

    if max_drawdown is not None and args.high_water_mark is not None:
        if args.drawdown_floor is not None:
            remaining_dd = args.high_water_mark - args.drawdown_floor
        else:
            remaining_dd = max_drawdown  # Cannot compute without floor

        drawdown_info["remaining"] = round(remaining_dd, 2)

        if pnl is not None and pnl < 0:
            effective_remaining = remaining_dd + pnl
            drawdown_info["effective_remaining"] = round(effective_remaining, 2)

            if effective_remaining <= 0:
                output["violations"].append(
                    f"DRAWDOWN BREACH: Effective remaining drawdown ${effective_remaining:.2f} "
                    f"(max: ${max_drawdown})"
                )
                output["compliant"] = False
            elif effective_remaining < max_drawdown * 0.25:
                output["warnings"].append(
                    f"Within 25% of drawdown limit: ${effective_remaining:.2f} remaining "
                    f"(max: ${max_drawdown})"
                )

    output["drawdown"] = drawdown_info

    # 5. Consistency rule
    consistency_rule = firm_data.get("consistency_rule")
    consistency = check_consistency(
        daily_pnl=args.daily_pnl if args.daily_pnl is not None else args.pnl,
        total_profit=args.total_profit,
        consistency_rule=consistency_rule,
        is_eval=args.is_eval,
    )
    output["consistency"] = consistency

    if consistency and not consistency["compliant"]:
        output["violations"].append(consistency["warning"])
        output["compliant"] = False
    elif consistency and consistency.get("warning") and consistency["status"] == "warning":
        output["warnings"].append(consistency["warning"])

    # 6. Overnight check (for EOD mode)
    if args.eod:
        if not firm_data.get("overnight_allowed", False):
            output["warnings"].append(
                "Reminder: Overnight positions NOT allowed. Ensure all positions are closed."
            )

    # 7. News blackout
    if firm_data.get("news_blackout"):
        minutes = firm_data.get("news_blackout_minutes", 2)
        output["warnings"].append(
            f"News blackout rule active: Must be flat {minutes} min before/after major news events."
        )

    # Summary
    output["rules_applied"] = {
        "profit_target": rules.get("profit_target"),
        "max_drawdown": max_drawdown,
        "daily_loss_limit": daily_loss_limit,
        "max_contracts": max_contracts,
        "close_by": close_by,
        "overnight_allowed": firm_data.get("overnight_allowed"),
        "consistency_rule": consistency_rule.get("description") if consistency_rule else None,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
