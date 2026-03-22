#!/usr/bin/env python3
"""
strategy_optimizer.py - Auto-find better strategy alternatives.
Args: --strategy (name), --diary-path.
1. Read the failing strategy's config and live performance
2. Generate variants by modifying filters, parameters, instruments
3. Backtest each variant
4. Rank by expectancy improvement
5. Output JSON + markdown report with comparison table and recommendation
"""

import argparse
import json
import os
import sys
import copy
import random
from datetime import datetime
from pathlib import Path


def load_strategy_config(diary_path, strategy_name):
    """Load strategy config from the strategies directory."""
    config_path = Path(diary_path) / "backtests" / "strategies" / f"{strategy_name}.json"
    if not config_path.exists():
        return None, f"Strategy config not found: {config_path}"
    try:
        with open(config_path, "r") as f:
            return json.load(f), None
    except (json.JSONDecodeError, OSError) as e:
        return None, f"Error reading strategy config: {e}"


def load_live_performance(diary_path, strategy_name):
    """Load live performance data for the strategy."""
    # Try loading from forward test results
    ft_path = Path(diary_path) / "backtests" / "forward-tests" / f"{strategy_name}-live.json"
    if ft_path.exists():
        try:
            with open(ft_path, "r") as f:
                return json.load(f), None
        except (json.JSONDecodeError, OSError):
            pass

    # Try computing from trade logs
    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))
    try:
        from forward_test_compare import find_strategy_trades, compute_rolling_metrics
        trades = find_strategy_trades(diary_path, strategy_name)
        if trades:
            metrics = compute_rolling_metrics(trades, window=min(len(trades), 30))
            return {"metrics": metrics, "total_trades": len(trades)}, None
    except ImportError:
        pass

    return None, "Could not load live performance data"


def generate_variants(config, n_variants=6):
    """Generate parameter variants of the original strategy."""
    variants = []
    entry_rules = config.get("entry_rules", {})
    stop_rules = config.get("stop_rules", {})
    target_rules = config.get("target_rules", {})

    # Variant 1: Tighter stops (smaller ATR multiplier)
    v1 = copy.deepcopy(config)
    v1["name"] = f"{config.get('name', 'unnamed')}_tight_stop"
    v1["variant_description"] = "Tighter stop loss (ATR multiplier reduced)"
    orig_atr_mult = stop_rules.get("atr_multiplier", 1.5)
    v1.setdefault("stop_rules", {})["atr_multiplier"] = max(0.5, orig_atr_mult * 0.7)
    variants.append(v1)

    # Variant 2: Wider stops (larger ATR multiplier)
    v2 = copy.deepcopy(config)
    v2["name"] = f"{config.get('name', 'unnamed')}_wide_stop"
    v2["variant_description"] = "Wider stop loss (ATR multiplier increased)"
    v2.setdefault("stop_rules", {})["atr_multiplier"] = orig_atr_mult * 1.5
    variants.append(v2)

    # Variant 3: Higher R target
    v3 = copy.deepcopy(config)
    v3["name"] = f"{config.get('name', 'unnamed')}_high_target"
    v3["variant_description"] = "Higher R:R target (3:1 instead of 2:1)"
    v3.setdefault("target_rules", {})["r_multiple"] = 3.0
    variants.append(v3)

    # Variant 4: Add trend filter
    v4 = copy.deepcopy(config)
    v4["name"] = f"{config.get('name', 'unnamed')}_trend_filter"
    v4["variant_description"] = "Added trend alignment filter (EMA)"
    v4.setdefault("entry_rules", {}).setdefault("filters", {})["trend_aligned"] = True
    variants.append(v4)

    # Variant 5: Different EMA periods
    v5 = copy.deepcopy(config)
    v5["name"] = f"{config.get('name', 'unnamed')}_fast_emas"
    v5["variant_description"] = "Faster EMA periods (5/13 instead of 9/21)"
    v5.setdefault("entry_rules", {})["ema_fast"] = 5
    v5.setdefault("entry_rules", {})["ema_slow"] = 13
    variants.append(v5)

    # Variant 6: RSI filter bounds
    v6 = copy.deepcopy(config)
    v6["name"] = f"{config.get('name', 'unnamed')}_rsi_filter"
    v6["variant_description"] = "Added RSI filter (avoid extremes: 35-65)"
    v6.setdefault("entry_rules", {}).setdefault("filters", {})["rsi_min"] = 35
    v6.setdefault("entry_rules", {}).setdefault("filters", {})["rsi_max"] = 65
    variants.append(v6)

    return variants[:n_variants]


def run_backtest_variant(config, account_size=50000):
    """Run a backtest for a strategy variant. Returns results dict."""
    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))

    try:
        from backtest_strategy import (
            fetch_data, build_strategy_class, safe_import_backtesting,
            safe_import_pandas, format_stats, extract_trade_returns,
            monte_carlo_simulation, safe_float,
        )
    except ImportError as e:
        return {"error": f"Could not import backtest_strategy: {e}"}

    pd, np = safe_import_pandas()
    if pd is None:
        return {"error": "pandas not installed"}

    BacktestClass, StrategyBase = safe_import_backtesting()
    if BacktestClass is None:
        return {"error": "backtesting library not installed"}

    # Fetch data
    instrument = config.get("instrument", "ES1!")
    exchange = config.get("exchange", "CME")
    timeframe = config.get("timeframe", "1h")
    data_range = config.get("data_range", {})

    data, err = fetch_data(instrument, exchange, timeframe, data_range.get("start"), data_range.get("end"))
    if err:
        return {"error": err}

    # Build and run strategy
    try:
        StrategyClass = build_strategy_class(config, data, StrategyBase)
        commission = config.get("commission", 0.002)
        bt = BacktestClass(data, StrategyClass, cash=account_size, commission=commission)
        stats = bt.run()

        result = format_stats(stats)
        trade_returns = extract_trade_returns(stats)

        # Quick Monte Carlo
        if trade_returns and len(trade_returns) >= 5:
            mc, _ = monte_carlo_simulation(trade_returns, account_size, n_runs=200)
            result["monte_carlo_p5_profitable"] = (mc.get("percentiles", {}).get("p5_return_pct", -1) or -1) > 0 if mc else False
            result["probability_profitable"] = mc.get("probability_profitable") if mc else None

        return result

    except Exception as e:
        return {"error": str(e)}


def rank_variants(original_results, variant_results):
    """Rank variants by improvement in key metrics vs original."""
    ranked = []

    orig_expectancy = original_results.get("Expectancy [%]") or 0
    orig_pf = original_results.get("Profit Factor") or 0
    orig_wr = original_results.get("Win Rate [%]") or 0
    orig_sharpe = original_results.get("Sharpe Ratio") or 0

    for name, results in variant_results.items():
        if "error" in results:
            ranked.append({
                "name": name,
                "error": results["error"],
                "score": -999,
            })
            continue

        exp = results.get("Expectancy [%]") or 0
        pf = results.get("Profit Factor") or 0
        wr = results.get("Win Rate [%]") or 0
        sharpe = results.get("Sharpe Ratio") or 0

        # Composite improvement score (weighted)
        exp_improvement = (exp - orig_expectancy) / max(abs(orig_expectancy), 0.01)
        pf_improvement = (pf - orig_pf) / max(abs(orig_pf), 0.01)
        sharpe_improvement = (sharpe - orig_sharpe) / max(abs(orig_sharpe), 0.01)

        score = exp_improvement * 0.4 + pf_improvement * 0.3 + sharpe_improvement * 0.3

        ranked.append({
            "name": name,
            "score": round(score, 4),
            "expectancy": exp,
            "expectancy_change": round(exp - orig_expectancy, 4),
            "profit_factor": pf,
            "win_rate": wr,
            "sharpe": sharpe,
            "trades": results.get("# Trades", 0),
            "return_pct": results.get("Return [%]"),
            "max_drawdown_pct": results.get("Max. Drawdown [%]"),
            "mc_profitable": results.get("probability_profitable"),
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked


def generate_report(output, original_config, original_results, rankings):
    """Generate a markdown comparison report."""
    lines = []
    lines.append(f"# Strategy Optimization Report")
    lines.append(f"**Original Strategy:** {original_config.get('name', 'unnamed')}")
    lines.append(f"**Date:** {output['timestamp']}")
    lines.append("")

    # Original performance
    lines.append("## Original Strategy Performance")
    lines.append(f"- Expectancy: {original_results.get('Expectancy [%]', 'N/A')}%")
    lines.append(f"- Profit Factor: {original_results.get('Profit Factor', 'N/A')}")
    lines.append(f"- Win Rate: {original_results.get('Win Rate [%]', 'N/A')}%")
    lines.append(f"- Sharpe Ratio: {original_results.get('Sharpe Ratio', 'N/A')}")
    lines.append(f"- Trades: {original_results.get('# Trades', 'N/A')}")
    lines.append("")

    # Comparison table
    lines.append("## Variant Comparison")
    lines.append("| Variant | Score | Expectancy | PF | Win Rate | Sharpe | Trades | DD% |")
    lines.append("|---------|-------|------------|-----|----------|--------|--------|-----|")
    lines.append(
        f"| **{original_config.get('name', 'orig')}** (original) | - "
        f"| {original_results.get('Expectancy [%]', 'N/A')} "
        f"| {original_results.get('Profit Factor', 'N/A')} "
        f"| {original_results.get('Win Rate [%]', 'N/A')} "
        f"| {original_results.get('Sharpe Ratio', 'N/A')} "
        f"| {original_results.get('# Trades', 'N/A')} "
        f"| {original_results.get('Max. Drawdown [%]', 'N/A')} |"
    )
    for r in rankings:
        if "error" in r:
            lines.append(f"| {r['name']} | ERROR | {r.get('error', '')} | | | | | |")
        else:
            lines.append(
                f"| {r['name']} "
                f"| {r['score']} "
                f"| {r['expectancy']} "
                f"| {r['profit_factor']} "
                f"| {r['win_rate']} "
                f"| {r['sharpe']} "
                f"| {r['trades']} "
                f"| {r.get('max_drawdown_pct', 'N/A')} |"
            )
    lines.append("")

    # Recommendation
    lines.append("## Recommendation")
    if rankings and rankings[0].get("score", 0) > 0:
        best = rankings[0]
        lines.append(f"**Best variant: {best['name']}** (improvement score: {best['score']})")
        lines.append(f"- Expectancy change: {best.get('expectancy_change', 'N/A')}")
        lines.append(f"- Recommend setting up forward test for this variant.")
    else:
        lines.append("No variant showed meaningful improvement. Consider:")
        lines.append("- Changing the underlying setup type")
        lines.append("- Testing on a different instrument or timeframe")
        lines.append("- Reviewing if market regime has changed")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Auto-optimize a trading strategy")
    parser.add_argument("--strategy", required=True, help="Strategy name to optimize")
    parser.add_argument("--diary-path", required=True, help="Path to diary directory")
    parser.add_argument("--account-size", type=float, default=50000, help="Account size (default: 50000)")
    parser.add_argument("--n-variants", type=int, default=6, help="Number of variants to test (default: 6)")
    parser.add_argument("--output-report", default=None, help="Path to save markdown report")
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "strategy": args.strategy,
        "original_performance": None,
        "live_performance": None,
        "variants_tested": 0,
        "rankings": [],
        "best_variant": None,
        "recommendation": None,
        "report": None,
        "error": None,
    }

    # Load original strategy config
    config, err = load_strategy_config(args.diary_path, args.strategy)
    if err:
        output["error"] = err
        print(json.dumps(output, indent=2))
        return

    # Load live performance (for context)
    live_perf, live_err = load_live_performance(args.diary_path, args.strategy)
    if live_perf:
        output["live_performance"] = live_perf.get("metrics") if isinstance(live_perf, dict) else live_perf

    # Run backtest on original config
    original_results = run_backtest_variant(config, args.account_size)
    if "error" in original_results:
        output["error"] = f"Original strategy backtest failed: {original_results['error']}"
        print(json.dumps(output, indent=2))
        return

    output["original_performance"] = original_results

    # Generate and test variants
    variants = generate_variants(config, args.n_variants)
    variant_results = {}

    for variant in variants:
        variant_name = variant.get("name", "unknown")
        results = run_backtest_variant(variant, args.account_size)
        variant_results[variant_name] = results
        output["variants_tested"] += 1

    # Rank variants
    rankings = rank_variants(original_results, variant_results)
    output["rankings"] = rankings

    # Best variant
    if rankings and rankings[0].get("score", 0) > 0 and "error" not in rankings[0]:
        best = rankings[0]
        output["best_variant"] = {
            "name": best["name"],
            "improvement_score": best["score"],
            "expectancy": best["expectancy"],
            "expectancy_change": best.get("expectancy_change"),
            "profit_factor": best["profit_factor"],
            "win_rate": best["win_rate"],
        }

        # Find the variant config
        for v in variants:
            if v.get("name") == best["name"]:
                output["best_variant"]["description"] = v.get("variant_description", "N/A")
                output["best_variant"]["config_changes"] = {
                    k: v[k] for k in v if k not in config or v[k] != config.get(k)
                }
                break

        output["recommendation"] = (
            f"REPLACE: Switch from '{args.strategy}' to '{best['name']}'. "
            f"Expected improvement: {best.get('expectancy_change', 'N/A')} in expectancy. "
            f"Set up a forward test with at least 50 trades before going live."
        )
    else:
        output["best_variant"] = None
        output["recommendation"] = (
            "NO IMPROVEMENT FOUND: None of the tested variants meaningfully outperform the original. "
            "Consider changing the setup type, instrument, or timeframe entirely."
        )

    # Generate markdown report
    report = generate_report(output, config, original_results, rankings)
    output["report"] = report

    # Save report if requested
    if args.output_report:
        try:
            report_path = Path(args.output_report)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w") as f:
                f.write(report)
            output["report_saved"] = str(report_path)
        except Exception as e:
            output["report_save_error"] = str(e)

    # Remove the full report text from JSON output to keep it clean
    # (it's saved to file if requested)
    if args.output_report:
        del output["report"]

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
