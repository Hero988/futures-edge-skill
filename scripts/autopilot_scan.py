#!/usr/bin/env python3
"""
autopilot_scan.py - Combined scan for autopilot: tvDatafeed bars + Scanner API real-time price.

Gets 15m bars from tvDatafeed for EMA/RSI calculation, then cross-checks the current
price against the TradingView Scanner API (which returns real-time data on the daily interval).

If the two prices diverge by more than --max-divergence, the Scanner API price is used
and a warning is flagged.

Outputs JSON with: price, EMA9, EMA21, RSI(14), ATR(14), VWAP, bar data, and data quality info.
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests


# --- Exchange mappings ---
EXCHANGE_MAP = {
    "ES1!": "CME_MINI", "MES1!": "CME_MINI",
    "NQ1!": "CME_MINI", "MNQ1!": "CME_MINI",
    "YM1!": "CBOT_MINI", "MYM1!": "CBOT_MINI",
    "RTY1!": "CME_MINI", "M2K1!": "CME_MINI",
    "CL1!": "NYMEX", "MCL1!": "NYMEX",
    "GC1!": "COMEX", "MGC1!": "COMEX",
}

SCANNER_URL = "https://scanner.tradingview.com/futures/scan"


def get_scanner_price(symbol):
    """Get real-time price from TradingView Scanner API (daily interval)."""
    exchange = EXCHANGE_MAP.get(symbol, "CME")
    payload = {
        "symbols": {"tickers": [f"{exchange}:{symbol}"], "query": {"types": []}},
        "columns": ["close", "open", "high", "low", "volume",
                     "Recommend.All", "Recommend.MA", "Recommend.Other",
                     "RSI", "EMA10", "EMA20", "MACD.macd", "MACD.signal",
                     "ADX", "ATR", "VWAP"],
    }
    try:
        resp = requests.post(SCANNER_URL, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("data", []):
            vals = item["d"]
            return {
                "price": vals[0],
                "open": vals[1],
                "high": vals[2],
                "low": vals[3],
                "volume": vals[4],
                "rec_all": vals[5],
                "rec_ma": vals[6],
                "rec_other": vals[7],
                "rsi_daily": vals[8],
                "ema10_daily": vals[9],
                "ema20_daily": vals[10],
                "macd_daily": vals[11],
                "macd_signal_daily": vals[12],
                "adx_daily": vals[13],
                "atr_daily": vals[14],
                "vwap_daily": vals[15],
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "No data returned"}


def compute_ema(closes, period):
    """Compute EMA for the given period. Returns list of EMA values."""
    if len(closes) < period:
        return []
    multiplier = 2.0 / (period + 1)
    ema = [sum(closes[:period]) / period]  # SMA seed
    for i in range(period, len(closes)):
        ema.append(closes[i] * multiplier + ema[-1] * (1 - multiplier))
    return ema


def compute_rsi(closes, period=14):
    """Compute RSI(period). Returns the last RSI value."""
    if len(closes) < period + 1:
        return None
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [max(d, 0) for d in deltas]
    losses = [abs(min(d, 0)) for d in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)


def compute_atr(highs, lows, closes, period=14):
    """Compute ATR(period). Returns the last ATR value."""
    if len(highs) < period + 1:
        return None
    true_ranges = []
    for i in range(1, len(highs)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        true_ranges.append(tr)
    if len(true_ranges) < period:
        return None
    atr = sum(true_ranges[:period]) / period
    for i in range(period, len(true_ranges)):
        atr = (atr * (period - 1) + true_ranges[i]) / period
    return round(atr, 4)


def compute_vwap_today(df):
    """Compute VWAP for today's bars only."""
    try:
        df_copy = df.copy()
        df_copy["date"] = df_copy.index.date
        today = df_copy["date"].iloc[-1]
        today_data = df_copy[df_copy["date"] == today]
        if len(today_data) == 0:
            return None
        cum_vp = 0.0
        cum_vol = 0.0
        for _, row in today_data.iterrows():
            tp = (row["high"] + row["low"] + row["close"]) / 3.0
            vol = row["volume"] if row["volume"] > 0 else 0
            cum_vp += tp * vol
            cum_vol += vol
        if cum_vol == 0:
            return None
        return round(cum_vp / cum_vol, 2)
    except Exception:
        return None


def detect_crossover(ema_fast, ema_slow):
    """Detect if EMA fast crossed above or below EMA slow in recent bars.
    EMA lists may have different lengths (EMA9 has more values than EMA21).
    We align them from the end (most recent bars).
    Returns: 'bullish', 'bearish', or 'none', plus bars ago of the cross."""
    if len(ema_fast) < 3 or len(ema_slow) < 3:
        return "none", None

    # Align from the end — both lists[-1] correspond to the same (latest) bar
    min_len = min(len(ema_fast), len(ema_slow))
    fast = ema_fast[-min_len:]
    slow = ema_slow[-min_len:]

    # Check last 10 bars for the most recent crossover
    check_range = min(10, min_len - 1)
    for i in range(1, check_range + 1):
        idx_curr = len(fast) - i
        idx_prev = idx_curr - 1
        if idx_prev < 0:
            break
        # Bullish: fast crosses above slow
        if fast[idx_prev] <= slow[idx_prev] and fast[idx_curr] > slow[idx_curr]:
            return "bullish", i
        # Bearish: fast crosses below slow
        if fast[idx_prev] >= slow[idx_prev] and fast[idx_curr] < slow[idx_curr]:
            return "bearish", i

    return "none", None


def load_tv_credentials():
    """Load TradingView credentials from config.json."""
    config_path = Path(__file__).resolve().parent.parent / "diary" / "config.json"
    try:
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            return config.get("tradingview_username"), config.get("tradingview_password")
    except Exception:
        pass
    return None, None


def get_bars(symbol, n_bars=60):
    """Get 15m bars from tvDatafeed. Returns DataFrame or None."""
    try:
        from tvDatafeed import TvDatafeed, Interval
    except ImportError:
        return None, "tvDatafeed not installed"

    exchange = EXCHANGE_MAP.get(symbol, "CME")
    username, password = load_tv_credentials()

    tv = None
    login_method = "nologin"
    for attempt in range(3):
        try:
            if username and password:
                tv = TvDatafeed(username=username, password=password)
                login_method = "authenticated"
            else:
                tv = TvDatafeed()
            time.sleep(1)
            break
        except Exception:
            time.sleep(2)

    if tv is None:
        return None, "Failed to connect to tvDatafeed"

    # Check if login actually worked
    # tvDatafeed silently falls back to nologin on auth failure
    # We detect this from stderr messages, but can't easily check programmatically
    # Just proceed and validate data quality downstream

    df = None
    for retry in range(3):
        try:
            df = tv.get_hist(
                symbol=symbol,
                exchange=exchange,
                interval=Interval.in_15_minute,
                n_bars=n_bars,
            )
            if df is not None and not df.empty:
                break
        except Exception:
            pass
        time.sleep(2)

    if df is None or df.empty:
        return None, "No bar data returned"

    df.columns = [c.lower().strip() for c in df.columns]
    return df, None


def main():
    parser = argparse.ArgumentParser(description="Autopilot scan: bars + real-time price cross-check")
    parser.add_argument("--symbol", default="CL1!", help="Symbol (default: CL1!)")
    parser.add_argument("--bars", type=int, default=60, help="Number of 15m bars (default: 60)")
    parser.add_argument("--max-divergence", type=float, default=0.20,
                        help="Max allowed price divergence between sources (default: $0.20)")
    args = parser.parse_args()

    output = {
        "timestamp": datetime.now().isoformat(),
        "symbol": args.symbol,
        "data_quality": "UNKNOWN",
        "price_source": "unknown",
        "scanner_price": None,
        "bars_price": None,
        "divergence": None,
        "price": None,
        "EMA9": None,
        "EMA21": None,
        "ema_gap_pct": None,
        "crossover": "none",
        "crossover_bars_ago": None,
        "RSI": None,
        "ATR": None,
        "VWAP": None,
        "daily": {},
        "recent_bars": [],
        "bar_high": None,
        "bar_low": None,
        "errors": [],
    }

    # --- Step 1: Get real-time price from Scanner API ---
    scanner = get_scanner_price(args.symbol)
    if "error" in scanner:
        output["errors"].append(f"Scanner API: {scanner['error']}")
    else:
        output["scanner_price"] = round(scanner["price"], 2)
        output["daily"] = {
            "recommendation": scanner.get("rec_all"),
            "rec_ma": scanner.get("rec_ma"),
            "rec_other": scanner.get("rec_other"),
            "rsi": round(scanner.get("rsi_daily", 0) or 0, 1),
            "ema10": round(scanner.get("ema10_daily", 0) or 0, 2),
            "ema20": round(scanner.get("ema20_daily", 0) or 0, 2),
            "macd": round(scanner.get("macd_daily", 0) or 0, 4),
            "macd_signal": round(scanner.get("macd_signal_daily", 0) or 0, 4),
            "adx": round(scanner.get("adx_daily", 0) or 0, 1),
            "atr": round(scanner.get("atr_daily", 0) or 0, 4),
            "vwap": round(scanner.get("vwap_daily", 0) or 0, 2),
            "day_high": round(scanner.get("high", 0) or 0, 2),
            "day_low": round(scanner.get("low", 0) or 0, 2),
        }

    # --- Step 2: Get 15m bars from tvDatafeed ---
    df, bar_err = get_bars(args.symbol, args.bars)
    if bar_err:
        output["errors"].append(f"tvDatafeed: {bar_err}")
    else:
        closes = df["close"].tolist()
        highs = df["high"].tolist()
        lows = df["low"].tolist()

        output["bars_price"] = round(closes[-1], 2)
        output["bar_high"] = round(highs[-1], 2)
        output["bar_low"] = round(lows[-1], 2)

        # Compute indicators from bars
        ema9_vals = compute_ema(closes, 9)
        ema21_vals = compute_ema(closes, 21)

        if ema9_vals:
            output["EMA9"] = round(ema9_vals[-1], 2)
        if ema21_vals:
            output["EMA21"] = round(ema21_vals[-1], 2)

        if output["EMA9"] and output["EMA21"] and output["EMA21"] != 0:
            output["ema_gap_pct"] = round(
                abs(output["EMA9"] - output["EMA21"]) / output["EMA21"] * 100, 3
            )

        # Crossover detection
        if ema9_vals and ema21_vals:
            cross_type, cross_bars = detect_crossover(ema9_vals, ema21_vals)
            output["crossover"] = cross_type
            output["crossover_bars_ago"] = cross_bars

        output["RSI"] = compute_rsi(closes, 14)
        output["ATR"] = compute_atr(highs, lows, closes, 14)
        output["VWAP"] = compute_vwap_today(df)

        # Last 5 bars for context
        for i in range(max(0, len(df) - 5), len(df)):
            output["recent_bars"].append({
                "time": str(df.index[i]),
                "open": round(float(df["open"].iloc[i]), 2),
                "high": round(float(highs[i]), 2),
                "low": round(float(lows[i]), 2),
                "close": round(float(closes[i]), 2),
                "volume": int(df["volume"].iloc[i]) if "volume" in df.columns else 0,
            })

    # --- Step 3: Cross-check prices and determine best source ---
    if output["scanner_price"] and output["bars_price"]:
        divergence = abs(output["scanner_price"] - output["bars_price"])
        output["divergence"] = round(divergence, 2)

        if divergence <= args.max_divergence:
            # Sources agree — use bars price (has the current bar context)
            output["price"] = output["bars_price"]
            output["price_source"] = "bars"
            output["data_quality"] = "GOOD"
        else:
            # Sources disagree — use Scanner API (real-time, more reliable)
            output["price"] = output["scanner_price"]
            output["price_source"] = "scanner_api"
            output["data_quality"] = "DEGRADED"
            output["errors"].append(
                f"Price divergence ${divergence:.2f} exceeds ${args.max_divergence:.2f} threshold. "
                f"Bars={output['bars_price']}, Scanner={output['scanner_price']}. Using Scanner API price."
            )
    elif output["scanner_price"]:
        output["price"] = output["scanner_price"]
        output["price_source"] = "scanner_api_only"
        output["data_quality"] = "DEGRADED"
    elif output["bars_price"]:
        output["price"] = output["bars_price"]
        output["price_source"] = "bars_only"
        output["data_quality"] = "DEGRADED"
    else:
        output["data_quality"] = "FAILED"
        output["errors"].append("No price data from any source")

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
