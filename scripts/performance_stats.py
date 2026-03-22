#!/usr/bin/env python3
"""
performance_stats.py - Compute performance metrics from diary trade logs.
Args: --diary-path, --period (day/week/month/all), --date (reference date).
Reads trade log markdown files, parses P&L and R-multiple values.
Outputs JSON with comprehensive metrics to stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_date_arg(date_str):
    """Parse date argument, supporting 'today' and date strings."""
    if date_str is None or date_str.lower() == "today":
        return datetime.now().date()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return datetime.now().date()


def get_date_range(period, ref_date):
    """Return (start_date, end_date) for the given period."""
    if period == "day":
        return ref_date, ref_date
    elif period == "week":
        # Monday to Sunday week containing ref_date
        start = ref_date - timedelta(days=ref_date.weekday())
        end = start + timedelta(days=6)
        return start, end
    elif period == "month":
        start = ref_date.replace(day=1)
        # Last day of month
        if ref_date.month == 12:
            end = ref_date.replace(year=ref_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end = ref_date.replace(month=ref_date.month + 1, day=1) - timedelta(days=1)
        return start, end
    else:  # "all"
        return datetime(2020, 1, 1).date(), datetime(2030, 12, 31).date()


def find_trade_files(diary_path, start_date, end_date):
    """Find all trade log files within the date range."""
    trade_files = []
    diary = Path(diary_path)

    if not diary.exists():
        return trade_files

    # Walk through diary/{YYYY}/{MM}/{YYYY-MM-DD}/trades/
    for year_dir in sorted(diary.iterdir()):
        if not year_dir.is_dir() or year_dir.name.startswith(".") or year_dir.name in ("lessons", "stats", "backtests", "config.json"):
            continue

        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue

            for day_dir in sorted(month_dir.iterdir()):
                if not day_dir.is_dir():
                    continue

                # Parse date from directory name
                try:
                    dir_date = datetime.strptime(day_dir.name, "%Y-%m-%d").date()
                except ValueError:
                    continue

                if dir_date < start_date or dir_date > end_date:
                    continue

                trades_dir = day_dir / "trades"
                if trades_dir.exists() and trades_dir.is_dir():
                    for tf in sorted(trades_dir.iterdir()):
                        if tf.suffix == ".md" and tf.name.startswith("trade-"):
                            trade_files.append((dir_date, tf))

    return trade_files


def parse_trade_log(filepath):
    """Parse a trade log markdown file and extract key metrics."""
    trade = {
        "file": str(filepath),
        "date": None,
        "instrument": None,
        "direction": None,
        "setup": None,
        "session": None,
        "pnl": None,
        "r_multiple": None,
        "result": None,  # win/loss/breakeven
        "contracts": None,
        "entry_price": None,
        "exit_price": None,
        "stop_price": None,
        "target_price": None,
        "grade": None,
        "strategy": None,
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return trade

    # Extract values using regex patterns on markdown content
    patterns = {
        "instrument": [
            r"[Ii]nstrument[:\s]*\*?\*?([A-Z0-9!]+)",
            r"[Cc]ontract[:\s]*\*?\*?([A-Z0-9!]+)",
            r"[Ss]ymbol[:\s]*\*?\*?([A-Z0-9!]+)",
        ],
        "direction": [
            r"[Dd]irection[:\s]*\*?\*?(long|short|Long|Short|LONG|SHORT)",
            r"[Ss]ide[:\s]*\*?\*?(long|short|buy|sell|Long|Short|Buy|Sell)",
        ],
        "setup": [
            r"[Ss]etup[:\s]*\*?\*?(.+?)(?:\n|\||\*)",
            r"[Ss]trategy[:\s]*\*?\*?(.+?)(?:\n|\||\*)",
        ],
        "session": [
            r"[Ss]ession[:\s]*\*?\*?([\w\s]+?)(?:\n|\||\*)",
        ],
        "pnl": [
            r"[Pp](?:&|n)[Ll][:\s]*\$?\*?\*?([-+]?[\d,]+\.?\d*)",
            r"[Pp]rofit[/\s][Ll]oss[:\s]*\$?\*?\*?([-+]?[\d,]+\.?\d*)",
            r"[Rr]esult[:\s]*\$?\*?\*?([-+]?[\d,]+\.?\d*)",
            r"[Nn]et[:\s]*\$?\*?\*?([-+]?[\d,]+\.?\d*)",
        ],
        "r_multiple": [
            r"[Rr][-\s]?[Mm]ultiple[:\s]*\*?\*?([-+]?[\d.]+)\s*[Rr]?",
            r"([-+]?[\d.]+)\s*[Rr]\b",
        ],
        "contracts": [
            r"[Cc]ontracts?[:\s]*\*?\*?(\d+)",
            r"[Ss]ize[:\s]*\*?\*?(\d+)",
            r"[Qq]uantity[:\s]*\*?\*?(\d+)",
        ],
        "entry_price": [
            r"[Ee]ntry[:\s]*\$?\*?\*?([\d,]+\.?\d*)",
        ],
        "exit_price": [
            r"[Ee]xit[:\s]*\$?\*?\*?([\d,]+\.?\d*)",
        ],
        "stop_price": [
            r"[Ss]top[:\s]*\$?\*?\*?([\d,]+\.?\d*)",
        ],
        "grade": [
            r"[Gg]rade[:\s]*\*?\*?([A-Fa-f][+-]?)",
        ],
        "strategy": [
            r"[Ss]trategy[:\s]*\*?\*?(.+?)(?:\n|\||\*)",
        ],
    }

    for field, pats in patterns.items():
        for pat in pats:
            match = re.search(pat, content)
            if match:
                val = match.group(1).strip().rstrip("*")
                if field in ("pnl", "entry_price", "exit_price", "stop_price", "target_price"):
                    try:
                        trade[field] = float(val.replace(",", ""))
                    except ValueError:
                        pass
                elif field == "r_multiple":
                    try:
                        trade[field] = float(val)
                    except ValueError:
                        pass
                elif field == "contracts":
                    try:
                        trade[field] = int(val)
                    except ValueError:
                        pass
                elif field == "direction":
                    trade[field] = val.lower()
                else:
                    trade[field] = val
                break

    # Determine win/loss/breakeven
    if trade["pnl"] is not None:
        if trade["pnl"] > 0:
            trade["result"] = "win"
        elif trade["pnl"] < 0:
            trade["result"] = "loss"
        else:
            trade["result"] = "breakeven"
    elif trade["r_multiple"] is not None:
        if trade["r_multiple"] > 0:
            trade["result"] = "win"
        elif trade["r_multiple"] < 0:
            trade["result"] = "loss"
        else:
            trade["result"] = "breakeven"

    return trade


def compute_stats(trades):
    """Compute comprehensive performance statistics from parsed trades."""
    stats = {
        "total_trades": len(trades),
        "total_pnl": 0.0,
        "total_r": 0.0,
        "wins": 0,
        "losses": 0,
        "breakevens": 0,
        "win_rate": 0.0,
        "avg_win_pnl": 0.0,
        "avg_loss_pnl": 0.0,
        "avg_win_r": 0.0,
        "avg_loss_r": 0.0,
        "profit_factor": 0.0,
        "largest_win": 0.0,
        "largest_loss": 0.0,
        "largest_win_r": 0.0,
        "largest_loss_r": 0.0,
        "consecutive_wins": 0,
        "consecutive_losses": 0,
        "max_consecutive_wins": 0,
        "max_consecutive_losses": 0,
        "expectancy": 0.0,
        "expectancy_r": 0.0,
        "by_setup": {},
        "by_session": {},
        "by_contract": {},
        "by_direction": {"long": {"trades": 0, "pnl": 0, "wins": 0}, "short": {"trades": 0, "pnl": 0, "wins": 0}},
    }

    if not trades:
        return stats

    win_pnls = []
    loss_pnls = []
    win_rs = []
    loss_rs = []
    current_streak = 0
    streak_type = None

    for t in trades:
        pnl = t.get("pnl") or 0.0
        r_mult = t.get("r_multiple") or 0.0
        result = t.get("result")

        stats["total_pnl"] += pnl
        stats["total_r"] += r_mult

        if result == "win":
            stats["wins"] += 1
            win_pnls.append(pnl)
            if r_mult > 0:
                win_rs.append(r_mult)
            if streak_type == "win":
                current_streak += 1
            else:
                current_streak = 1
                streak_type = "win"
            stats["max_consecutive_wins"] = max(stats["max_consecutive_wins"], current_streak)
        elif result == "loss":
            stats["losses"] += 1
            loss_pnls.append(pnl)
            if r_mult < 0:
                loss_rs.append(r_mult)
            if streak_type == "loss":
                current_streak += 1
            else:
                current_streak = 1
                streak_type = "loss"
            stats["max_consecutive_losses"] = max(stats["max_consecutive_losses"], current_streak)
        else:
            stats["breakevens"] += 1
            current_streak = 0
            streak_type = None

        # Track last streak
        if streak_type == "win":
            stats["consecutive_wins"] = current_streak
            stats["consecutive_losses"] = 0
        elif streak_type == "loss":
            stats["consecutive_losses"] = current_streak
            stats["consecutive_wins"] = 0

        # By setup
        setup = t.get("setup") or "unknown"
        if setup not in stats["by_setup"]:
            stats["by_setup"][setup] = {"trades": 0, "wins": 0, "pnl": 0.0, "r": 0.0}
        stats["by_setup"][setup]["trades"] += 1
        stats["by_setup"][setup]["pnl"] += pnl
        stats["by_setup"][setup]["r"] += r_mult
        if result == "win":
            stats["by_setup"][setup]["wins"] += 1

        # By session
        session = t.get("session") or "unknown"
        if session not in stats["by_session"]:
            stats["by_session"][session] = {"trades": 0, "wins": 0, "pnl": 0.0, "r": 0.0}
        stats["by_session"][session]["trades"] += 1
        stats["by_session"][session]["pnl"] += pnl
        stats["by_session"][session]["r"] += r_mult
        if result == "win":
            stats["by_session"][session]["wins"] += 1

        # By contract
        instrument = t.get("instrument") or "unknown"
        if instrument not in stats["by_contract"]:
            stats["by_contract"][instrument] = {"trades": 0, "wins": 0, "pnl": 0.0, "r": 0.0}
        stats["by_contract"][instrument]["trades"] += 1
        stats["by_contract"][instrument]["pnl"] += pnl
        stats["by_contract"][instrument]["r"] += r_mult
        if result == "win":
            stats["by_contract"][instrument]["wins"] += 1

        # By direction
        direction = t.get("direction") or "unknown"
        if direction in stats["by_direction"]:
            stats["by_direction"][direction]["trades"] += 1
            stats["by_direction"][direction]["pnl"] += pnl
            if result == "win":
                stats["by_direction"][direction]["wins"] += 1

    # Compute derived metrics
    decided_trades = stats["wins"] + stats["losses"]
    if decided_trades > 0:
        stats["win_rate"] = round(stats["wins"] / decided_trades * 100, 2)

    if win_pnls:
        stats["avg_win_pnl"] = round(sum(win_pnls) / len(win_pnls), 2)
        stats["largest_win"] = round(max(win_pnls), 2)
    if loss_pnls:
        stats["avg_loss_pnl"] = round(sum(loss_pnls) / len(loss_pnls), 2)
        stats["largest_loss"] = round(min(loss_pnls), 2)
    if win_rs:
        stats["avg_win_r"] = round(sum(win_rs) / len(win_rs), 2)
        stats["largest_win_r"] = round(max(win_rs), 2)
    if loss_rs:
        stats["avg_loss_r"] = round(sum(loss_rs) / len(loss_rs), 2)
        stats["largest_loss_r"] = round(min(loss_rs), 2)

    # Profit factor
    gross_profit = sum(win_pnls) if win_pnls else 0
    gross_loss = abs(sum(loss_pnls)) if loss_pnls else 0
    if gross_loss > 0:
        stats["profit_factor"] = round(gross_profit / gross_loss, 2)
    elif gross_profit > 0:
        stats["profit_factor"] = float("inf")

    # Expectancy
    if decided_trades > 0:
        wr = stats["wins"] / decided_trades
        avg_win = stats["avg_win_pnl"] if win_pnls else 0
        avg_loss = abs(stats["avg_loss_pnl"]) if loss_pnls else 0
        stats["expectancy"] = round(wr * avg_win - (1 - wr) * avg_loss, 2)

        avg_win_r = stats["avg_win_r"] if win_rs else 0
        avg_loss_r = abs(stats["avg_loss_r"]) if loss_rs else 0
        stats["expectancy_r"] = round(wr * avg_win_r - (1 - wr) * avg_loss_r, 4)

    # Compute win rates for sub-categories
    for category in ["by_setup", "by_session", "by_contract"]:
        for key, data in stats[category].items():
            if data["trades"] > 0:
                data["win_rate"] = round(data["wins"] / data["trades"] * 100, 2)
                data["pnl"] = round(data["pnl"], 2)
                data["r"] = round(data["r"], 2)

    stats["total_pnl"] = round(stats["total_pnl"], 2)
    stats["total_r"] = round(stats["total_r"], 2)

    return stats


def main():
    parser = argparse.ArgumentParser(description="Compute performance stats from trade logs")
    parser.add_argument(
        "--diary-path",
        required=True,
        help="Path to diary directory",
    )
    parser.add_argument(
        "--period",
        choices=["day", "week", "month", "all"],
        default="all",
        help="Period to analyze (default: all)",
    )
    parser.add_argument(
        "--date",
        default="today",
        help="Reference date (YYYY-MM-DD or 'today', default: today)",
    )
    args = parser.parse_args()

    ref_date = parse_date_arg(args.date)
    start_date, end_date = get_date_range(args.period, ref_date)

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "period": args.period,
        "date_range": {
            "start": str(start_date),
            "end": str(end_date),
            "reference": str(ref_date),
        },
        "stats": None,
        "trades_parsed": 0,
        "parse_errors": 0,
        "error": None,
    }

    # Find trade files
    trade_files = find_trade_files(args.diary_path, start_date, end_date)

    if not trade_files:
        output["stats"] = compute_stats([])
        output["error"] = f"No trade files found in {args.diary_path} for period {args.period} ({start_date} to {end_date})"
        print(json.dumps(output, indent=2))
        return

    # Parse trades
    trades = []
    for trade_date, filepath in trade_files:
        trade = parse_trade_log(filepath)
        trade["date"] = str(trade_date)
        if trade.get("pnl") is not None or trade.get("r_multiple") is not None:
            trades.append(trade)
            output["trades_parsed"] += 1
        else:
            output["parse_errors"] += 1

    # Compute statistics
    output["stats"] = compute_stats(trades)

    # Include per-day breakdown
    daily = {}
    for t in trades:
        d = t.get("date", "unknown")
        if d not in daily:
            daily[d] = {"trades": 0, "pnl": 0.0, "r": 0.0, "wins": 0, "losses": 0}
        daily[d]["trades"] += 1
        daily[d]["pnl"] += t.get("pnl") or 0
        daily[d]["r"] += t.get("r_multiple") or 0
        if t.get("result") == "win":
            daily[d]["wins"] += 1
        elif t.get("result") == "loss":
            daily[d]["losses"] += 1

    for d in daily.values():
        d["pnl"] = round(d["pnl"], 2)
        d["r"] = round(d["r"], 2)

    output["daily_breakdown"] = daily

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
