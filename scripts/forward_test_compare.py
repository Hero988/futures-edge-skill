#!/usr/bin/env python3
"""
forward_test_compare.py - Compare live trades against backtest baseline.
Args: --strategy (name), --diary-path.
Reads baseline from diary/backtests/baselines/{name}.json.
Reads live trades tagged with this strategy from trade logs.
Computes rolling metrics and compares to baseline confidence bands.
Outputs JSON to stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


def load_baseline(diary_path, strategy_name):
    """Load the backtest baseline for a strategy."""
    baseline_path = Path(diary_path) / "backtests" / "baselines" / f"{strategy_name}.json"
    if not baseline_path.exists():
        return None, f"Baseline not found: {baseline_path}"
    try:
        with open(baseline_path, "r") as f:
            return json.load(f), None
    except (json.JSONDecodeError, OSError) as e:
        return None, f"Error reading baseline: {e}"


def find_strategy_trades(diary_path, strategy_name):
    """Find all trades tagged with the given strategy."""
    diary = Path(diary_path)
    trades = []

    if not diary.exists():
        return trades

    for year_dir in sorted(diary.iterdir()):
        if not year_dir.is_dir() or year_dir.name.startswith(".") or year_dir.name in ("lessons", "stats", "backtests", "config.json"):
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for day_dir in sorted(month_dir.iterdir()):
                if not day_dir.is_dir():
                    continue
                try:
                    dir_date = datetime.strptime(day_dir.name, "%Y-%m-%d").date()
                except ValueError:
                    continue

                trades_dir = day_dir / "trades"
                if not trades_dir.exists():
                    continue

                for tf in sorted(trades_dir.iterdir()):
                    if not tf.suffix == ".md":
                        continue

                    try:
                        with open(tf, "r", encoding="utf-8") as f:
                            content = f.read()
                    except (OSError, UnicodeDecodeError):
                        continue

                    # Check if trade is tagged with this strategy
                    strategy_patterns = [
                        r"[Ss]trategy[:\s]*\*?\*?(.+?)(?:\n|\||\*)",
                        r"[Ss]etup[:\s]*\*?\*?(.+?)(?:\n|\||\*)",
                    ]
                    matched = False
                    for pat in strategy_patterns:
                        match = re.search(pat, content)
                        if match:
                            found_strategy = match.group(1).strip().lower().replace(" ", "-").rstrip("*")
                            if strategy_name.lower() in found_strategy or found_strategy in strategy_name.lower():
                                matched = True
                                break

                    if not matched:
                        continue

                    # Parse trade metrics
                    trade = {"date": str(dir_date), "file": str(tf)}

                    # P&L
                    pnl_match = re.search(r"[Pp](?:&|n)[Ll][:\s]*\$?\*?\*?([-+]?[\d,]+\.?\d*)", content)
                    if pnl_match:
                        try:
                            trade["pnl"] = float(pnl_match.group(1).replace(",", ""))
                        except ValueError:
                            trade["pnl"] = None
                    else:
                        trade["pnl"] = None

                    # R-multiple
                    r_match = re.search(r"[Rr][-\s]?[Mm]ultiple[:\s]*\*?\*?([-+]?[\d.]+)", content)
                    if r_match:
                        try:
                            trade["r_multiple"] = float(r_match.group(1))
                        except ValueError:
                            trade["r_multiple"] = None
                    else:
                        trade["r_multiple"] = None

                    # Result
                    if trade["pnl"] is not None:
                        trade["result"] = "win" if trade["pnl"] > 0 else ("loss" if trade["pnl"] < 0 else "breakeven")
                    elif trade["r_multiple"] is not None:
                        trade["result"] = "win" if trade["r_multiple"] > 0 else ("loss" if trade["r_multiple"] < 0 else "breakeven")
                    else:
                        trade["result"] = None

                    trades.append(trade)

    return trades


def compute_rolling_metrics(trades, window=20):
    """Compute rolling metrics over the last `window` trades."""
    if not trades:
        return None

    recent = trades[-window:] if len(trades) >= window else trades
    n = len(recent)

    wins = sum(1 for t in recent if t.get("result") == "win")
    losses = sum(1 for t in recent if t.get("result") == "loss")
    decided = wins + losses

    total_pnl = sum(t.get("pnl", 0) or 0 for t in recent)
    total_r = sum(t.get("r_multiple", 0) or 0 for t in recent)

    win_pnls = [t["pnl"] for t in recent if t.get("result") == "win" and t.get("pnl") is not None]
    loss_pnls = [t["pnl"] for t in recent if t.get("result") == "loss" and t.get("pnl") is not None]

    win_rate = (wins / decided * 100) if decided > 0 else 0
    avg_win = sum(win_pnls) / len(win_pnls) if win_pnls else 0
    avg_loss = abs(sum(loss_pnls) / len(loss_pnls)) if loss_pnls else 0
    profit_factor = (sum(win_pnls) / abs(sum(loss_pnls))) if loss_pnls and sum(loss_pnls) != 0 else float("inf") if win_pnls else 0

    # Expectancy
    if decided > 0:
        wr = wins / decided
        expectancy = wr * avg_win - (1 - wr) * avg_loss
    else:
        expectancy = 0

    # Max drawdown in the window
    equity = 0
    peak = 0
    max_dd = 0
    for t in recent:
        pnl = t.get("pnl", 0) or 0
        equity += pnl
        if equity > peak:
            peak = equity
        dd = peak - equity
        if dd > max_dd:
            max_dd = dd

    return {
        "window_size": n,
        "total_trades": n,
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2),
        "total_r": round(total_r, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "profit_factor": round(profit_factor, 2) if profit_factor != float("inf") else "inf",
        "expectancy": round(expectancy, 2),
        "max_drawdown": round(max_dd, 2),
    }


def compare_to_baseline(live_metrics, baseline):
    """Compare live metrics against baseline confidence bands."""
    comparisons = {}

    # Expected baseline fields
    baseline_metrics = baseline.get("metrics", baseline)

    # Win rate comparison
    live_wr = live_metrics.get("win_rate", 0)
    bl_wr = baseline_metrics.get("win_rate", {})
    if isinstance(bl_wr, dict):
        wr_low = bl_wr.get("low", bl_wr.get("p25", 0))
        wr_high = bl_wr.get("high", bl_wr.get("p75", 100))
        wr_median = bl_wr.get("median", bl_wr.get("p50", 50))
    else:
        wr_median = float(bl_wr) if bl_wr else 50
        wr_low = wr_median * 0.8
        wr_high = wr_median * 1.2

    comparisons["win_rate"] = {
        "live": live_wr,
        "baseline_low": round(wr_low, 2),
        "baseline_high": round(wr_high, 2),
        "baseline_median": round(wr_median, 2),
        "status": "GREEN" if wr_low <= live_wr <= wr_high else ("YELLOW" if live_wr >= wr_low * 0.9 else "RED"),
    }

    # Profit factor comparison
    live_pf = live_metrics.get("profit_factor", 0)
    if live_pf == "inf":
        live_pf = 999
    bl_pf = baseline_metrics.get("profit_factor", {})
    if isinstance(bl_pf, dict):
        pf_low = bl_pf.get("low", 1.0)
        pf_high = bl_pf.get("high", 3.0)
        pf_median = bl_pf.get("median", 1.5)
    else:
        pf_median = float(bl_pf) if bl_pf else 1.5
        pf_low = pf_median * 0.7
        pf_high = pf_median * 1.3

    comparisons["profit_factor"] = {
        "live": live_pf if live_pf != 999 else "inf",
        "baseline_low": round(pf_low, 2),
        "baseline_high": round(pf_high, 2),
        "status": "GREEN" if live_pf >= pf_low else ("YELLOW" if live_pf >= pf_low * 0.8 else "RED"),
    }

    # Expectancy comparison
    live_exp = live_metrics.get("expectancy", 0)
    bl_exp = baseline_metrics.get("expectancy", {})
    if isinstance(bl_exp, dict):
        exp_low = bl_exp.get("low", 0)
        exp_high = bl_exp.get("high", 100)
    else:
        exp_median = float(bl_exp) if bl_exp else 50
        exp_low = exp_median * 0.7
        exp_high = exp_median * 1.3

    comparisons["expectancy"] = {
        "live": live_exp,
        "baseline_low": round(exp_low, 2),
        "baseline_high": round(exp_high, 2),
        "status": "GREEN" if live_exp >= exp_low else ("YELLOW" if live_exp >= exp_low * 0.8 else "RED"),
    }

    # Max drawdown comparison
    live_dd = live_metrics.get("max_drawdown", 0)
    bl_dd = baseline_metrics.get("max_drawdown", {})
    if isinstance(bl_dd, dict):
        dd_threshold = bl_dd.get("threshold", bl_dd.get("p95", 5000))
    else:
        dd_threshold = float(bl_dd) * 1.5 if bl_dd else 5000

    comparisons["max_drawdown"] = {
        "live": live_dd,
        "baseline_threshold": round(dd_threshold, 2),
        "status": "GREEN" if live_dd <= dd_threshold else ("YELLOW" if live_dd <= dd_threshold * 1.25 else "RED"),
    }

    # Overall health
    statuses = [c["status"] for c in comparisons.values()]
    if "RED" in statuses:
        overall = "RED"
    elif statuses.count("YELLOW") >= 2:
        overall = "YELLOW"
    elif "YELLOW" in statuses:
        overall = "YELLOW"
    else:
        overall = "GREEN"

    return comparisons, overall


def main():
    parser = argparse.ArgumentParser(description="Compare live trades against backtest baseline")
    parser.add_argument("--strategy", required=True, help="Strategy name")
    parser.add_argument("--diary-path", required=True, help="Path to diary directory")
    parser.add_argument("--window", type=int, default=20, help="Rolling window size (default: 20)")
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "strategy": args.strategy,
        "total_trades": 0,
        "metrics": None,
        "comparison": None,
        "overall_health": None,
        "alerts": [],
        "error": None,
    }

    # Load baseline
    baseline, bl_err = load_baseline(args.diary_path, args.strategy)
    if bl_err:
        output["error"] = bl_err
        # Still try to compute live metrics even without baseline
        baseline = None

    # Find live trades
    trades = find_strategy_trades(args.diary_path, args.strategy)
    output["total_trades"] = len(trades)

    if not trades:
        output["error"] = (output.get("error") or "") + f" No live trades found for strategy '{args.strategy}'."
        output["overall_health"] = "INSUFFICIENT_DATA"
        print(json.dumps(output, indent=2))
        return

    # Compute rolling metrics
    metrics = compute_rolling_metrics(trades, window=args.window)
    output["metrics"] = metrics

    # Compare to baseline
    if baseline:
        comparisons, overall = compare_to_baseline(metrics, baseline)
        output["comparison"] = comparisons
        output["overall_health"] = overall

        # Generate alerts
        for metric_name, comparison in comparisons.items():
            if comparison["status"] == "RED":
                output["alerts"].append(
                    f"ALERT: {metric_name} is RED - live value {comparison['live']} is outside baseline bands"
                )
            elif comparison["status"] == "YELLOW":
                output["alerts"].append(
                    f"WARNING: {metric_name} is YELLOW - live value {comparison['live']} is near baseline boundary"
                )

        if overall == "RED":
            output["alerts"].append(
                "STRATEGY DEGRADATION DETECTED: Consider running strategy_optimizer.py for alternatives."
            )
    else:
        output["overall_health"] = "NO_BASELINE"
        output["alerts"].append("No baseline available for comparison. Run a backtest first to establish baseline.")

    # Additional context
    if len(trades) < 20:
        output["alerts"].append(
            f"Only {len(trades)} trades recorded. Minimum 50 recommended for reliable comparison."
        )

    output["trade_dates"] = {
        "first": trades[0]["date"] if trades else None,
        "last": trades[-1]["date"] if trades else None,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
