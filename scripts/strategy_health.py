#!/usr/bin/env python3
"""
strategy_health.py - Monitor all active forward tests.
Args: --diary-path, --all-strategies.
Scans diary/backtests/forward-tests/ for active tests.
For each, computes health status against baseline.
Outputs JSON to stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def find_active_forward_tests(diary_path):
    """Find all active forward test configs."""
    ft_dir = Path(diary_path) / "backtests" / "forward-tests"
    tests = []

    if not ft_dir.exists():
        return tests

    for f in sorted(ft_dir.iterdir()):
        if f.suffix == ".json" and f.name.endswith("-live.json"):
            try:
                with open(f, "r") as fh:
                    config = json.load(fh)
                strategy_name = f.stem.replace("-live", "")
                config["_strategy_name"] = strategy_name
                config["_file"] = str(f)
                tests.append(config)
            except (json.JSONDecodeError, OSError):
                tests.append({
                    "_strategy_name": f.stem.replace("-live", ""),
                    "_file": str(f),
                    "_error": "Could not parse forward test config",
                })

    return tests


def find_all_strategies_from_baselines(diary_path):
    """Find all strategies that have baselines (even if no forward test config)."""
    baselines_dir = Path(diary_path) / "backtests" / "baselines"
    strategies = []

    if not baselines_dir.exists():
        return strategies

    for f in sorted(baselines_dir.iterdir()):
        if f.suffix == ".json":
            strategies.append(f.stem)

    return strategies


def run_forward_test_compare(strategy_name, diary_path, window=20):
    """Run forward test comparison for a single strategy.
    This reimplements the core logic to avoid subprocess calls.
    """
    # Import the comparison logic
    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))

    try:
        from forward_test_compare import load_baseline, find_strategy_trades, compute_rolling_metrics, compare_to_baseline
    except ImportError:
        return {
            "strategy": strategy_name,
            "error": "Could not import forward_test_compare module",
            "health": "UNKNOWN",
        }

    result = {
        "strategy": strategy_name,
        "total_trades": 0,
        "health": "UNKNOWN",
        "alerts": [],
        "metrics": None,
        "comparison": None,
    }

    # Load baseline
    baseline, bl_err = load_baseline(diary_path, strategy_name)

    # Find trades
    trades = find_strategy_trades(diary_path, strategy_name)
    result["total_trades"] = len(trades)

    if not trades:
        result["health"] = "NO_DATA"
        result["alerts"].append(f"No trades found for strategy '{strategy_name}'")
        return result

    # Compute metrics
    metrics = compute_rolling_metrics(trades, window=window)
    result["metrics"] = metrics

    # Compare to baseline
    if baseline:
        comparisons, overall = compare_to_baseline(metrics, baseline)
        result["comparison"] = comparisons
        result["health"] = overall

        for metric_name, comp in comparisons.items():
            if comp["status"] == "RED":
                result["alerts"].append(f"{metric_name}: RED (live={comp['live']})")
            elif comp["status"] == "YELLOW":
                result["alerts"].append(f"{metric_name}: YELLOW (live={comp['live']})")
    else:
        result["health"] = "NO_BASELINE"
        if bl_err:
            result["alerts"].append(bl_err)

    if len(trades) < 20:
        result["alerts"].append(f"Low sample size: {len(trades)} trades (minimum 50 recommended)")

    return result


def main():
    parser = argparse.ArgumentParser(description="Monitor all active forward tests")
    parser.add_argument("--diary-path", required=True, help="Path to diary directory")
    parser.add_argument("--all-strategies", action="store_true", help="Check all strategies with baselines")
    parser.add_argument("--window", type=int, default=20, help="Rolling window for metrics (default: 20)")
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "strategies": [],
        "overall_status": "UNKNOWN",
        "total_strategies": 0,
        "summary": {
            "green": 0,
            "yellow": 0,
            "red": 0,
            "no_data": 0,
            "no_baseline": 0,
        },
        "error": None,
    }

    # Determine which strategies to check
    strategy_names = set()

    # From forward test configs
    active_tests = find_active_forward_tests(args.diary_path)
    for test in active_tests:
        name = test.get("_strategy_name")
        if name:
            strategy_names.add(name)

    # Also include all strategies with baselines if requested
    if args.all_strategies:
        baseline_strategies = find_all_strategies_from_baselines(args.diary_path)
        strategy_names.update(baseline_strategies)

    if not strategy_names:
        output["error"] = (
            "No active forward tests or baselines found. "
            f"Checked: {args.diary_path}/backtests/forward-tests/ and {args.diary_path}/backtests/baselines/"
        )
        print(json.dumps(output, indent=2))
        return

    output["total_strategies"] = len(strategy_names)

    # Run comparison for each strategy
    for name in sorted(strategy_names):
        result = run_forward_test_compare(name, args.diary_path, window=args.window)
        output["strategies"].append(result)

        health = result.get("health", "UNKNOWN")
        if health == "GREEN":
            output["summary"]["green"] += 1
        elif health == "YELLOW":
            output["summary"]["yellow"] += 1
        elif health == "RED":
            output["summary"]["red"] += 1
        elif health == "NO_DATA":
            output["summary"]["no_data"] += 1
        elif health == "NO_BASELINE":
            output["summary"]["no_baseline"] += 1

    # Determine overall status
    if output["summary"]["red"] > 0:
        output["overall_status"] = "RED"
    elif output["summary"]["yellow"] > 0:
        output["overall_status"] = "YELLOW"
    elif output["summary"]["green"] > 0:
        output["overall_status"] = "GREEN"
    else:
        output["overall_status"] = "INSUFFICIENT_DATA"

    # Top-level alerts
    red_strategies = [s["strategy"] for s in output["strategies"] if s.get("health") == "RED"]
    if red_strategies:
        output["critical_alert"] = f"Strategies requiring immediate attention: {', '.join(red_strategies)}"

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
