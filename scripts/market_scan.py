#!/usr/bin/env python3
"""
market_scan.py - Scan futures symbols using TradingView's scanner API directly.
Args: --symbols (list), --exchange (default CME), --intervals (list, default "1h 4h 1d").
Outputs JSON with technical analysis summary and key indicators per symbol+interval.
"""

import argparse
import json
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests library not installed. Run: pip install requests"}))
    sys.exit(1)

# TradingView exchange mapping for futures symbols
FUTURES_EXCHANGE_MAP = {
    "ES1!": "CME_MINI", "MES1!": "CME_MINI",
    "NQ1!": "CME_MINI", "MNQ1!": "CME_MINI",
    "YM1!": "CBOT_MINI", "MYM1!": "CBOT_MINI",
    "RTY1!": "CME_MINI", "M2K1!": "CME_MINI",
    "CL1!": "NYMEX", "MCL1!": "NYMEX",
    "GC1!": "COMEX", "MGC1!": "COMEX",
    "SI1!": "COMEX", "ZN1!": "CBOT",
    "ZB1!": "CBOT", "NG1!": "NYMEX",
    "6E1!": "CME", "6B1!": "CME", "6J1!": "CME",
}

# Interval to TradingView column suffix mapping
# TradingView scanner uses different column names per timeframe
INTERVAL_SUFFIX = {
    "1m": "|1",
    "5m": "|5",
    "15m": "|15",
    "30m": "|30",
    "1h": "|60",
    "2h": "|120",
    "4h": "|240",
    "1d": "",       # Daily is the default (no suffix)
    "1w": "|1W",
    "1M": "|1M",
}

# Columns to request from TradingView scanner
BASE_COLUMNS = [
    "close", "open", "high", "low", "volume",
    "RSI", "MACD.macd", "MACD.signal",
    "EMA10", "EMA20", "EMA50", "EMA200", "SMA20",
    "Stoch.K", "Stoch.D", "CCI20", "ADX", "ATR",
    "BB.upper", "BB.lower",
    "Pivot.M.Classic.Middle", "Pivot.M.Classic.R1", "Pivot.M.Classic.R2",
    "Pivot.M.Classic.S1", "Pivot.M.Classic.S2",
    "Recommend.All", "Recommend.MA", "Recommend.Other",
    "VWAP",
]

SCANNER_URL = "https://scanner.tradingview.com/futures/scan"


def recommendation_label(value):
    """Convert TradingView numeric recommendation to label."""
    if value is None:
        return "UNKNOWN"
    if value >= 0.5:
        return "STRONG_BUY"
    elif value >= 0.1:
        return "BUY"
    elif value > -0.1:
        return "NEUTRAL"
    elif value > -0.5:
        return "SELL"
    else:
        return "STRONG_SELL"


def safe_round(val, decimals=4):
    """Safely round a value, returning None for non-numeric."""
    if val is None:
        return None
    try:
        return round(float(val), decimals)
    except (TypeError, ValueError):
        return None


def scan_symbols(symbols, interval="1d"):
    """Scan multiple symbols at a given interval using TradingView scanner API."""
    suffix = INTERVAL_SUFFIX.get(interval, "")

    # Build column list with interval suffix
    columns = [f"{col}{suffix}" for col in BASE_COLUMNS]

    # Build tickers list with exchange prefix
    tickers = []
    for sym in symbols:
        exchange = FUTURES_EXCHANGE_MAP.get(sym, "CME")
        tickers.append(f"{exchange}:{sym}")

    payload = {
        "symbols": {"tickers": tickers, "query": {"types": []}},
        "columns": columns,
    }

    try:
        resp = requests.post(SCANNER_URL, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        return None, str(e)

    results = {}
    for item in data.get("data", []):
        ticker = item["s"]  # e.g. "CME_MINI:ES1!"
        symbol = ticker.split(":")[-1] if ":" in ticker else ticker
        values = item["d"]

        # Map values to indicator names
        indicators = {}
        col_names = [
            "close", "open", "high", "low", "volume",
            "RSI", "MACD_macd", "MACD_signal",
            "EMA10", "EMA20", "EMA50", "EMA200", "SMA20",
            "Stoch_K", "Stoch_D", "CCI", "ADX", "ATR",
            "BB_upper", "BB_lower",
            "Pivot_P", "Pivot_R1", "Pivot_R2",
            "Pivot_S1", "Pivot_S2",
            "Recommend_All", "Recommend_MA", "Recommend_Other",
            "VWAP",
        ]

        for name, val in zip(col_names, values):
            indicators[name] = safe_round(val)

        # Build summary from recommendation values
        rec_all = indicators.get("Recommend_All")
        rec_ma = indicators.get("Recommend_MA")
        rec_other = indicators.get("Recommend_Other")

        summary = {
            "recommendation": recommendation_label(rec_all),
            "recommendation_value": rec_all,
            "ma_recommendation": recommendation_label(rec_ma),
            "oscillator_recommendation": recommendation_label(rec_other),
        }

        results[symbol] = {
            "summary": summary,
            "indicators": indicators,
        }

    return results, None


def main():
    parser = argparse.ArgumentParser(description="Scan futures symbols with TradingView scanner")
    parser.add_argument(
        "--symbols", nargs="+", default=["ES1!"],
        help="TradingView symbols (e.g., ES1! NQ1! CL1! GC1!)",
    )
    parser.add_argument("--exchange", default="CME", help="Default exchange (auto-mapped for known futures)")
    parser.add_argument(
        "--intervals", nargs="+", default=["1h", "4h", "1d"],
        help="Intervals to scan (1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w, 1M)",
    )
    args = parser.parse_args()

    output = {
        "timestamp": datetime.now().isoformat(),
        "symbols": args.symbols,
        "intervals": args.intervals,
        "results": [],
        "errors": [],
    }

    for interval in args.intervals:
        if interval not in INTERVAL_SUFFIX:
            output["errors"].append({
                "interval": interval,
                "error": f"Invalid interval. Valid: {list(INTERVAL_SUFFIX.keys())}",
            })
            continue

        results, error = scan_symbols(args.symbols, interval)

        if error:
            output["errors"].append({"interval": interval, "error": error})
            continue

        for symbol in args.symbols:
            if symbol in results:
                # Find or create symbol entry
                sym_entry = None
                for r in output["results"]:
                    if r["symbol"] == symbol:
                        sym_entry = r
                        break
                if sym_entry is None:
                    sym_entry = {"symbol": symbol, "exchange": FUTURES_EXCHANGE_MAP.get(symbol, args.exchange), "intervals": {}}
                    output["results"].append(sym_entry)

                sym_entry["intervals"][interval] = results[symbol]
            else:
                output["errors"].append({
                    "symbol": symbol, "interval": interval,
                    "error": "Symbol not found in results",
                })

        # Small delay between interval requests to avoid rate limiting
        if len(args.intervals) > 1:
            time.sleep(0.5)

    output["scan_count"] = len(args.symbols) * len(args.intervals)
    output["success_count"] = sum(len(r["intervals"]) for r in output["results"])
    output["error_count"] = len(output["errors"])

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
