#!/usr/bin/env python3
"""
historical_data.py - Pull OHLCV data via tvDatafeed and compute key levels.
Args: --symbol, --exchange, --interval, --bars, --config-path.
Reads TradingView credentials from config.json if available.
Computes: PDH/PDL/PDC, weekly high/low, ATR(14), swing highs/lows, VWAP.
Outputs JSON to stdout.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


INTERVAL_MAP = {
    "1m": "in_1_minute",
    "5m": "in_5_minute",
    "15m": "in_15_minute",
    "1h": "in_1_hour",
    "4h": "in_4_hour",
    "1d": "in_daily",
    "1w": "in_weekly",
}

# Exchange mapping for futures (tvDatafeed needs the correct exchange)
EXCHANGE_MAP = {
    "ES1!": "CME_MINI", "MES1!": "CME_MINI",
    "NQ1!": "CME_MINI", "MNQ1!": "CME_MINI",
    "YM1!": "CBOT_MINI", "MYM1!": "CBOT_MINI",
    "RTY1!": "CME_MINI", "M2K1!": "CME_MINI",
    "CL1!": "NYMEX", "MCL1!": "NYMEX",
    "GC1!": "COMEX", "MGC1!": "COMEX",
}


def load_tv_credentials(config_path=None):
    """Load TradingView credentials from config.json."""
    paths_to_try = []
    if config_path:
        paths_to_try.append(Path(config_path))
    # Default: ../diary/config.json relative to this script
    paths_to_try.append(Path(__file__).resolve().parent.parent / "diary" / "config.json")

    for p in paths_to_try:
        try:
            if p.exists():
                with open(p, "r") as f:
                    config = json.load(f)
                username = config.get("tradingview_username")
                password = config.get("tradingview_password")
                if username and password:
                    return username, password
        except (json.JSONDecodeError, OSError):
            continue

    return None, None


def get_tv_interval(interval_str):
    """Map user interval string to tvDatafeed Interval enum member."""
    try:
        from tvDatafeed import Interval
    except ImportError:
        return None, "tvDatafeed not installed. Run install_deps.py first."

    attr_name = INTERVAL_MAP.get(interval_str)
    if attr_name is None:
        return None, f"Invalid interval '{interval_str}'. Valid: {list(INTERVAL_MAP.keys())}"

    return getattr(Interval, attr_name, None), None


def compute_atr(highs, lows, closes, period=14):
    """Compute ATR(period) from arrays. Returns the last ATR value."""
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

    # Initial ATR = simple average of first `period` TRs
    atr = sum(true_ranges[:period]) / period

    # Smooth using Wilder's method
    for i in range(period, len(true_ranges)):
        atr = (atr * (period - 1) + true_ranges[i]) / period

    return round(atr, 4)


def find_swing_highs(highs, lookback=5, count=5):
    """Find swing highs: a bar whose high is higher than `lookback` bars on each side."""
    swings = []
    for i in range(lookback, len(highs) - lookback):
        is_swing = True
        for j in range(1, lookback + 1):
            if highs[i] <= highs[i - j] or highs[i] <= highs[i + j]:
                is_swing = False
                break
        if is_swing:
            swings.append({"index": i, "price": round(highs[i], 4)})

    # Return last `count` swing highs
    return swings[-count:] if len(swings) >= count else swings


def find_swing_lows(lows, lookback=5, count=5):
    """Find swing lows: a bar whose low is lower than `lookback` bars on each side."""
    swings = []
    for i in range(lookback, len(lows) - lookback):
        is_swing = True
        for j in range(1, lookback + 1):
            if lows[i] >= lows[i - j] or lows[i] >= lows[i + j]:
                is_swing = False
                break
        if is_swing:
            swings.append({"index": i, "price": round(lows[i], 4)})

    return swings[-count:] if len(swings) >= count else swings


def compute_vwap(highs, lows, closes, volumes):
    """Compute running VWAP. Returns the final VWAP value."""
    if len(highs) == 0 or volumes is None:
        return None

    cumulative_vp = 0.0
    cumulative_vol = 0.0

    for i in range(len(highs)):
        typical_price = (highs[i] + lows[i] + closes[i]) / 3.0
        vol = volumes[i] if volumes[i] is not None and volumes[i] > 0 else 0
        cumulative_vp += typical_price * vol
        cumulative_vol += vol

    if cumulative_vol == 0:
        return None

    return round(cumulative_vp / cumulative_vol, 4)


def get_previous_day_levels(df):
    """Extract previous day high/low/close from intraday data."""
    try:
        import pandas as pd

        if df.index.name == "datetime" or hasattr(df.index, "date"):
            df_copy = df.copy()
            df_copy["date"] = df_copy.index.date
            dates = sorted(df_copy["date"].unique())

            if len(dates) < 2:
                return None, None, None

            prev_date = dates[-2]
            prev_day = df_copy[df_copy["date"] == prev_date]

            pdh = round(float(prev_day["high"].max()), 4)
            pdl = round(float(prev_day["low"].min()), 4)
            pdc = round(float(prev_day["close"].iloc[-1]), 4)
            return pdh, pdl, pdc
    except Exception:
        pass

    return None, None, None


def get_weekly_levels(df):
    """Extract current/most recent week high/low from data."""
    try:
        import pandas as pd

        if df.index.name == "datetime" or hasattr(df.index, "date"):
            df_copy = df.copy()
            df_copy["date"] = df_copy.index.date

            # Get most recent week of data (last 5 trading days)
            dates = sorted(df_copy["date"].unique())
            if len(dates) < 5:
                week_dates = dates
            else:
                week_dates = dates[-5:]

            week_data = df_copy[df_copy["date"].isin(week_dates)]
            wh = round(float(week_data["high"].max()), 4)
            wl = round(float(week_data["low"].min()), 4)
            return wh, wl
    except Exception:
        pass

    return None, None


def main():
    parser = argparse.ArgumentParser(description="Pull OHLCV data and compute key levels")
    parser.add_argument("--symbol", default="ES1!", help="TradingView symbol (default: ES1!)")
    parser.add_argument("--exchange", default="CME", help="Exchange (default: CME)")
    parser.add_argument("--interval", default="1h", help="Interval (default: 1h)")
    parser.add_argument("--bars", type=int, default=500, help="Number of bars (default: 500)")
    parser.add_argument(
        "--swing-lookback",
        type=int,
        default=5,
        help="Bars on each side for swing detection (default: 5)",
    )
    parser.add_argument(
        "--config-path",
        default=None,
        help="Path to config.json for TradingView credentials (optional)",
    )
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "symbol": args.symbol,
        "exchange": args.exchange,
        "interval": args.interval,
        "bars_requested": args.bars,
        "bars_received": 0,
        "data": None,
        "levels": None,
        "error": None,
    }

    # Get the interval enum
    tv_interval, err = get_tv_interval(args.interval)
    if err:
        output["error"] = err
        print(json.dumps(output, indent=2))
        return

    # Resolve exchange via mapping
    effective_exchange = EXCHANGE_MAP.get(args.symbol, args.exchange)

    # Pull data
    try:
        from tvDatafeed import TvDatafeed, Interval
        import time as _time

        # Load TradingView credentials from config
        tv_username, tv_password = load_tv_credentials(args.config_path)

        # Retry logic: tvDatafeed websocket can fail on first attempt
        tv = None
        for _attempt in range(3):
            try:
                if tv_username and tv_password:
                    tv = TvDatafeed(username=tv_username, password=tv_password)
                else:
                    tv = TvDatafeed()  # no auth for delayed data
                _time.sleep(2)  # Let websocket stabilize
                break
            except Exception:
                _time.sleep(3)

        if tv is None:
            output["error"] = "Failed to connect to TvDatafeed after 3 attempts."
            print(json.dumps(output, indent=2))
            return

        df = None
        for _retry in range(3):
            df = tv.get_hist(
                symbol=args.symbol,
                exchange=effective_exchange,
                interval=tv_interval,
                n_bars=args.bars,
            )
            if df is not None and not df.empty:
                break
            _time.sleep(3)

        if df is None or df.empty:
            output["error"] = "No data returned from tvDatafeed. Symbol may be invalid or service unavailable."
            print(json.dumps(output, indent=2))
            return

    except ImportError:
        output["error"] = "tvDatafeed not installed. Run install_deps.py first."
        print(json.dumps(output, indent=2))
        return
    except Exception as e:
        output["error"] = f"tvDatafeed error: {str(e)}"
        print(json.dumps(output, indent=2))
        return

    # Convert data
    try:
        import pandas as pd
        import numpy as np

        # Normalize column names (tvDatafeed may use various casings)
        df.columns = [c.lower().strip() for c in df.columns]

        output["bars_received"] = len(df)

        highs = df["high"].tolist()
        lows = df["low"].tolist()
        closes = df["close"].tolist()
        opens = df["open"].tolist()
        volumes = df["volume"].tolist() if "volume" in df.columns else None

        # Current price info
        last_bar = {
            "datetime": str(df.index[-1]),
            "open": round(float(opens[-1]), 4),
            "high": round(float(highs[-1]), 4),
            "low": round(float(lows[-1]), 4),
            "close": round(float(closes[-1]), 4),
            "volume": int(volumes[-1]) if volumes else None,
        }

        # Compute levels
        atr14 = compute_atr(highs, lows, closes, period=14)

        swing_highs = find_swing_highs(highs, lookback=args.swing_lookback, count=5)
        swing_lows = find_swing_lows(lows, lookback=args.swing_lookback, count=5)

        pdh, pdl, pdc = get_previous_day_levels(df)
        weekly_high, weekly_low = get_weekly_levels(df)

        # VWAP (only meaningful for intraday data)
        vwap = None
        is_intraday = args.interval in ["1m", "5m", "15m", "1h", "4h"]
        if is_intraday and volumes:
            # Compute VWAP for today's bars only
            df_copy = df.copy()
            df_copy["date"] = df_copy.index.date
            today = df_copy["date"].iloc[-1]
            today_data = df_copy[df_copy["date"] == today]
            if len(today_data) > 0:
                vwap = compute_vwap(
                    today_data["high"].tolist(),
                    today_data["low"].tolist(),
                    today_data["close"].tolist(),
                    today_data["volume"].tolist(),
                )

        # Recent OHLCV bars (last 10 for context)
        recent_bars = []
        start_idx = max(0, len(df) - 10)
        for i in range(start_idx, len(df)):
            bar = {
                "datetime": str(df.index[i]),
                "open": round(float(opens[i]), 4),
                "high": round(float(highs[i]), 4),
                "low": round(float(lows[i]), 4),
                "close": round(float(closes[i]), 4),
            }
            if volumes:
                bar["volume"] = int(volumes[i]) if volumes[i] is not None else 0
            recent_bars.append(bar)

        output["data"] = {
            "last_bar": last_bar,
            "recent_bars": recent_bars,
        }

        output["levels"] = {
            "previous_day": {
                "high": pdh,
                "low": pdl,
                "close": pdc,
            },
            "weekly": {
                "high": weekly_high,
                "low": weekly_low,
            },
            "atr_14": atr14,
            "vwap": vwap,
            "swing_highs": swing_highs,
            "swing_lows": swing_lows,
            "data_range": {
                "start": str(df.index[0]),
                "end": str(df.index[-1]),
                "total_bars": len(df),
            },
        }

    except Exception as e:
        output["error"] = f"Data processing error: {str(e)}"

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
