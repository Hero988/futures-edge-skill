#!/usr/bin/env python3
"""
backtest_strategy.py - Backtesting engine with prop firm simulation.
Args: --config (path to strategy JSON), --prop-firm (optional), --account-size (optional).
Supports ICT concepts (via smartmoneyconcepts), indicator-based strategies, and prop firm simulation.
Includes in-sample/out-of-sample split, walk-forward, and Monte Carlo analysis.
Outputs JSON + optional markdown report to stdout.
"""

import argparse
import json
import os
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
import math

# ---------------------------------------------------------------------------
# Helper: safe import wrappers
# ---------------------------------------------------------------------------

def safe_import_pandas():
    try:
        import pandas as pd
        import numpy as np
        return pd, np
    except ImportError:
        return None, None

def safe_import_tvdatafeed():
    try:
        from tvDatafeed import TvDatafeed, Interval
        return TvDatafeed, Interval
    except ImportError:
        return None, None

def safe_import_backtesting():
    try:
        from backtesting import Backtest, Strategy
        return Backtest, Strategy
    except ImportError:
        return None, None

def safe_import_smc():
    try:
        import smartmoneyconcepts as smc
        return smc
    except ImportError:
        try:
            from smartmoneyconcepts import smc as smc_mod
            return smc_mod
        except ImportError:
            return None

# ---------------------------------------------------------------------------
# Data retrieval
# ---------------------------------------------------------------------------

INTERVAL_MAP = {
    "1m": "in_1_minute",
    "5m": "in_5_minute",
    "15m": "in_15_minute",
    "1h": "in_1_hour",
    "4h": "in_4_hour",
    "1d": "in_daily",
    "1w": "in_weekly",
}

def fetch_data(symbol, exchange, timeframe, start_date=None, end_date=None, n_bars=5000):
    """Fetch OHLCV data via tvDatafeed. Pull multiple chunks if needed."""
    TvDatafeed, Interval = safe_import_tvdatafeed()
    pd, np = safe_import_pandas()

    if TvDatafeed is None:
        return None, "tvDatafeed not installed. Run install_deps.py first."
    if pd is None:
        return None, "pandas not installed. Run install_deps.py first."

    attr_name = INTERVAL_MAP.get(timeframe)
    if attr_name is None:
        return None, f"Invalid timeframe '{timeframe}'. Valid: {list(INTERVAL_MAP.keys())}"

    tv_interval = getattr(Interval, attr_name, None)
    if tv_interval is None:
        return None, f"Interval attribute '{attr_name}' not found in tvDatafeed.Interval"

    try:
        tv = TvDatafeed()
        # Fetch data in chunks if needed (tvDatafeed max ~5000 bars per call)
        max_per_call = 5000
        all_data = []
        remaining = n_bars

        while remaining > 0:
            batch = min(remaining, max_per_call)
            df = tv.get_hist(
                symbol=symbol,
                exchange=exchange,
                interval=tv_interval,
                n_bars=batch,
            )
            if df is None or df.empty:
                break
            all_data.append(df)
            remaining -= len(df)
            if len(df) < batch:
                break  # No more data available

        if not all_data:
            return None, "No data returned from tvDatafeed."

        combined = pd.concat(all_data).drop_duplicates().sort_index()

        # Filter by date range if provided
        if start_date:
            try:
                start_dt = pd.Timestamp(start_date)
                combined = combined[combined.index >= start_dt]
            except Exception:
                pass
        if end_date:
            try:
                end_dt = pd.Timestamp(end_date)
                combined = combined[combined.index <= end_dt]
            except Exception:
                pass

        # Standardize column names for backtesting.py (needs Open, High, Low, Close, Volume)
        combined.columns = [c.strip().lower() for c in combined.columns]
        rename_map = {}
        for col in combined.columns:
            if "open" in col:
                rename_map[col] = "Open"
            elif "high" in col:
                rename_map[col] = "High"
            elif "low" in col:
                rename_map[col] = "Low"
            elif "close" in col:
                rename_map[col] = "Close"
            elif "volume" in col or "vol" in col:
                rename_map[col] = "Volume"
        combined.rename(columns=rename_map, inplace=True)

        # Ensure required columns
        for col in ["Open", "High", "Low", "Close"]:
            if col not in combined.columns:
                return None, f"Missing required column '{col}' in data."

        if "Volume" not in combined.columns:
            combined["Volume"] = 0

        return combined, None

    except Exception as e:
        return None, f"Data fetch error: {str(e)}"


# ---------------------------------------------------------------------------
# Indicator computation
# ---------------------------------------------------------------------------

def compute_ema(series, period):
    """Compute EMA of a pandas Series."""
    return series.ewm(span=period, adjust=False).mean()


def compute_sma(series, period):
    """Compute SMA of a pandas Series."""
    return series.rolling(window=period).mean()


def compute_rsi(series, period=14):
    """Compute RSI."""
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_atr(high, low, close, period=14):
    """Compute ATR."""
    pd, np = safe_import_pandas()
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def compute_vwap(high, low, close, volume):
    """Compute cumulative VWAP (resets not handled -- full series)."""
    tp = (high + low + close) / 3.0
    cumvp = (tp * volume).cumsum()
    cumvol = volume.cumsum()
    return cumvp / cumvol.replace(0, 1)


def compute_macd(close, fast=12, slow=26, signal=9):
    """Compute MACD line, signal line, and histogram."""
    ema_fast = compute_ema(close, fast)
    ema_slow = compute_ema(close, slow)
    macd_line = ema_fast - ema_slow
    signal_line = compute_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


# ---------------------------------------------------------------------------
# SMC signal detection
# ---------------------------------------------------------------------------

def detect_smc_signals(df, setup_type):
    """Use smartmoneyconcepts library to detect ICT signals. Returns a Series of signals."""
    pd, np = safe_import_pandas()
    smc = safe_import_smc()

    signals = pd.Series(0, index=df.index)

    if smc is None:
        return signals, "smartmoneyconcepts not installed. Run install_deps.py first."

    try:
        ohlc = df[["Open", "High", "Low", "Close"]].copy()
        ohlc.columns = ["open", "high", "low", "close"]

        if setup_type in ("bullish_order_block", "bearish_order_block"):
            try:
                ob_result = smc.ob(ohlc)
                if ob_result is not None and hasattr(ob_result, "__len__") and len(ob_result) > 0:
                    if isinstance(ob_result, pd.DataFrame):
                        if "OB" in ob_result.columns:
                            if setup_type == "bullish_order_block":
                                signals = (ob_result["OB"] == 1).astype(int)
                            else:
                                signals = (ob_result["OB"] == -1).astype(int)
                        elif "BullOB" in ob_result.columns and setup_type == "bullish_order_block":
                            signals = ob_result["BullOB"].fillna(0).astype(int)
                        elif "BearOB" in ob_result.columns and setup_type == "bearish_order_block":
                            signals = ob_result["BearOB"].fillna(0).astype(int)
            except Exception as e:
                return signals, f"SMC order block detection error: {e}"

        elif setup_type in ("bullish_fvg", "bearish_fvg"):
            try:
                fvg_result = smc.fvg(ohlc)
                if fvg_result is not None and isinstance(fvg_result, pd.DataFrame):
                    if "FVG" in fvg_result.columns:
                        if setup_type == "bullish_fvg":
                            signals = (fvg_result["FVG"] == 1).astype(int)
                        else:
                            signals = (fvg_result["FVG"] == -1).astype(int)
                    elif "BullFVG" in fvg_result.columns and setup_type == "bullish_fvg":
                        signals = fvg_result["BullFVG"].fillna(0).astype(int)
                    elif "BearFVG" in fvg_result.columns and setup_type == "bearish_fvg":
                        signals = fvg_result["BearFVG"].fillna(0).astype(int)
            except Exception as e:
                return signals, f"SMC FVG detection error: {e}"

        elif setup_type in ("bos_long", "bos_short"):
            try:
                bos_result = smc.bos(ohlc)
                if bos_result is not None and isinstance(bos_result, pd.DataFrame):
                    if "BOS" in bos_result.columns:
                        if setup_type == "bos_long":
                            signals = (bos_result["BOS"] == 1).astype(int)
                        else:
                            signals = (bos_result["BOS"] == -1).astype(int)
                    elif "BullBOS" in bos_result.columns and setup_type == "bos_long":
                        signals = bos_result["BullBOS"].fillna(0).astype(int)
                    elif "BearBOS" in bos_result.columns and setup_type == "bos_short":
                        signals = bos_result["BearBOS"].fillna(0).astype(int)
            except Exception as e:
                return signals, f"SMC BOS detection error: {e}"

    except Exception as e:
        return signals, f"SMC detection error: {e}"

    return signals, None


# ---------------------------------------------------------------------------
# Strategy builder
# ---------------------------------------------------------------------------

ICT_SETUPS = {"bullish_order_block", "bearish_order_block", "bullish_fvg", "bearish_fvg", "bos_long", "bos_short"}
INDICATOR_SETUPS = {"ema_cross", "vwap_bounce", "rsi_divergence", "macd_cross", "bollinger_bounce"}


def build_strategy_class(config, data, BacktestStrategy):
    """Dynamically build a Strategy subclass from the config."""
    pd, np = safe_import_pandas()
    entry_rules = config.get("entry_rules", {})
    stop_rules = config.get("stop_rules", {})
    target_rules = config.get("target_rules", {})
    setup_type = entry_rules.get("setup", "ema_cross")
    risk_pct = config.get("risk_per_trade_pct", 1.0) / 100.0

    class DynamicStrategy(BacktestStrategy):
        # Parameters (can be optimized)
        ema_fast = entry_rules.get("ema_fast", 9)
        ema_slow = entry_rules.get("ema_slow", 21)
        rsi_period = entry_rules.get("rsi_period", 14)
        rsi_oversold = entry_rules.get("rsi_oversold", 30)
        rsi_overbought = entry_rules.get("rsi_overbought", 70)
        atr_period = stop_rules.get("atr_period", 14)
        atr_multiplier = stop_rules.get("atr_multiplier", 1.5)
        target_r = target_rules.get("r_multiple", 2.0)

        def init(self):
            close = self.data.Close
            high = self.data.High
            low = self.data.Low
            volume = self.data.Volume

            # Common indicators
            self.ema_fast_line = self.I(compute_ema, pd.Series(close), self.ema_fast)
            self.ema_slow_line = self.I(compute_ema, pd.Series(close), self.ema_slow)
            self.rsi = self.I(compute_rsi, pd.Series(close), self.rsi_period)
            self.atr = self.I(compute_atr, pd.Series(high), pd.Series(low), pd.Series(close), self.atr_period)

            # Pre-compute SMC signals if needed
            if setup_type in ICT_SETUPS:
                full_df = pd.DataFrame({
                    "Open": data["Open"].values,
                    "High": data["High"].values,
                    "Low": data["Low"].values,
                    "Close": data["Close"].values,
                })
                smc_signals, smc_err = detect_smc_signals(full_df, setup_type)
                self.smc_signal = self.I(lambda: smc_signals.values)
                self._smc_error = smc_err
            else:
                self.smc_signal = None
                self._smc_error = None

            # VWAP
            if entry_rules.get("setup") == "vwap_bounce":
                self.vwap = self.I(compute_vwap, pd.Series(high), pd.Series(low), pd.Series(close), pd.Series(volume))

            # MACD
            if entry_rules.get("setup") == "macd_cross":
                macd_l, sig_l, hist = compute_macd(pd.Series(close))
                self.macd_line = self.I(lambda: macd_l.values)
                self.macd_signal = self.I(lambda: sig_l.values)

        def next(self):
            if self.position:
                return  # Already in a trade

            atr_val = self.atr[-1] if len(self.atr) > 0 else None
            if atr_val is None or atr_val <= 0 or math.isnan(atr_val):
                return

            entry_signal = False
            is_long = True

            # --- Signal detection ---
            if setup_type in ICT_SETUPS:
                if self.smc_signal is not None and len(self.smc_signal) > 0:
                    if self.smc_signal[-1] == 1:
                        entry_signal = True
                        is_long = setup_type in ("bullish_order_block", "bullish_fvg", "bos_long")

            elif setup_type == "ema_cross":
                if len(self.ema_fast_line) > 1 and len(self.ema_slow_line) > 1:
                    # Bullish cross
                    if self.ema_fast_line[-2] <= self.ema_slow_line[-2] and self.ema_fast_line[-1] > self.ema_slow_line[-1]:
                        entry_signal = True
                        is_long = True
                    # Bearish cross
                    elif self.ema_fast_line[-2] >= self.ema_slow_line[-2] and self.ema_fast_line[-1] < self.ema_slow_line[-1]:
                        entry_signal = True
                        is_long = False

            elif setup_type == "vwap_bounce":
                if hasattr(self, "vwap") and len(self.vwap) > 1:
                    price = self.data.Close[-1]
                    vwap_val = self.vwap[-1]
                    # Long if price bounces up from VWAP
                    if self.data.Low[-1] <= vwap_val and self.data.Close[-1] > vwap_val:
                        entry_signal = True
                        is_long = True
                    # Short if price rejects down from VWAP
                    elif self.data.High[-1] >= vwap_val and self.data.Close[-1] < vwap_val:
                        entry_signal = True
                        is_long = False

            elif setup_type == "rsi_divergence":
                if len(self.rsi) > 1:
                    if self.rsi[-1] < self.rsi_oversold:
                        entry_signal = True
                        is_long = True
                    elif self.rsi[-1] > self.rsi_overbought:
                        entry_signal = True
                        is_long = False

            elif setup_type == "macd_cross":
                if hasattr(self, "macd_line") and len(self.macd_line) > 1:
                    if self.macd_line[-2] <= self.macd_signal[-2] and self.macd_line[-1] > self.macd_signal[-1]:
                        entry_signal = True
                        is_long = True
                    elif self.macd_line[-2] >= self.macd_signal[-2] and self.macd_line[-1] < self.macd_signal[-1]:
                        entry_signal = True
                        is_long = False

            # --- Apply filters ---
            filters = entry_rules.get("filters", {})
            if entry_signal and filters:
                # Trend filter
                if filters.get("trend_aligned") and len(self.ema_slow_line) > 0:
                    if is_long and self.data.Close[-1] < self.ema_slow_line[-1]:
                        entry_signal = False
                    elif not is_long and self.data.Close[-1] > self.ema_slow_line[-1]:
                        entry_signal = False

                # RSI filter
                rsi_min = filters.get("rsi_min")
                rsi_max = filters.get("rsi_max")
                if rsi_min is not None and self.rsi[-1] < rsi_min:
                    entry_signal = False
                if rsi_max is not None and self.rsi[-1] > rsi_max:
                    entry_signal = False

            # --- Execute trade ---
            if entry_signal:
                stop_distance = atr_val * self.atr_multiplier

                if is_long:
                    sl = self.data.Close[-1] - stop_distance
                    tp = self.data.Close[-1] + stop_distance * self.target_r
                    self.buy(sl=sl, tp=tp)
                else:
                    sl = self.data.Close[-1] + stop_distance
                    tp = self.data.Close[-1] - stop_distance * self.target_r
                    self.sell(sl=sl, tp=tp)

    return DynamicStrategy


# ---------------------------------------------------------------------------
# Walk-forward analysis
# ---------------------------------------------------------------------------

def walk_forward_analysis(data, config, BacktestClass, StrategyClass, cash, commission,
                          optimize_months=3, test_months=1):
    """Run walk-forward optimization with rolling windows."""
    pd, np = safe_import_pandas()
    results = []

    if len(data) < 100:
        return results, "Insufficient data for walk-forward analysis."

    # Determine window sizes in bars (approximate)
    total_days = (data.index[-1] - data.index[0]).days
    bars_per_day = max(1, len(data) / max(1, total_days))
    opt_bars = int(optimize_months * 30 * bars_per_day)
    test_bars = int(test_months * 30 * bars_per_day)
    window_size = opt_bars + test_bars

    if window_size > len(data):
        return results, "Data too short for walk-forward windows."

    step = test_bars
    i = 0

    while i + window_size <= len(data):
        opt_data = data.iloc[i:i + opt_bars]
        test_data = data.iloc[i + opt_bars:i + opt_bars + test_bars]

        try:
            # Run on optimization window
            bt_opt = BacktestClass(opt_data, StrategyClass, cash=cash, commission=commission)
            opt_stats = bt_opt.run()

            # Run on test window
            bt_test = BacktestClass(test_data, StrategyClass, cash=cash, commission=commission)
            test_stats = bt_test.run()

            window_result = {
                "window": len(results) + 1,
                "opt_start": str(opt_data.index[0]),
                "opt_end": str(opt_data.index[-1]),
                "test_start": str(test_data.index[0]),
                "test_end": str(test_data.index[-1]),
                "opt_return_pct": safe_float(opt_stats.get("Return [%]")),
                "test_return_pct": safe_float(test_stats.get("Return [%]")),
                "opt_trades": safe_int(opt_stats.get("# Trades")),
                "test_trades": safe_int(test_stats.get("# Trades")),
                "opt_win_rate": safe_float(opt_stats.get("Win Rate [%]")),
                "test_win_rate": safe_float(test_stats.get("Win Rate [%]")),
            }
            results.append(window_result)
        except Exception as e:
            results.append({
                "window": len(results) + 1,
                "error": str(e),
            })

        i += step

    return results, None


# ---------------------------------------------------------------------------
# Monte Carlo simulation
# ---------------------------------------------------------------------------

def monte_carlo_simulation(trade_returns, initial_capital, n_runs=1000):
    """Reshuffle trade results and compute confidence bands."""
    pd, np = safe_import_pandas()

    if not trade_returns or len(trade_returns) < 5:
        return None, "Insufficient trades for Monte Carlo simulation."

    results = {
        "runs": n_runs,
        "trade_count": len(trade_returns),
        "percentiles": {},
        "probability_profitable": 0.0,
        "worst_drawdown_5th": None,
        "median_return": None,
    }

    final_equities = []
    max_drawdowns = []

    for _ in range(n_runs):
        shuffled = list(trade_returns)
        random.shuffle(shuffled)

        equity = initial_capital
        peak = equity
        max_dd = 0

        for ret in shuffled:
            equity += ret
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd

        final_equities.append(equity)
        max_drawdowns.append(max_dd)

    final_equities.sort()
    max_drawdowns.sort()

    # Percentiles
    for pct in [5, 10, 25, 50, 75, 90, 95]:
        idx = int(len(final_equities) * pct / 100)
        idx = min(idx, len(final_equities) - 1)
        results["percentiles"][f"p{pct}_equity"] = round(final_equities[idx], 2)
        results["percentiles"][f"p{pct}_return_pct"] = round(
            (final_equities[idx] - initial_capital) / initial_capital * 100, 2
        )

    results["probability_profitable"] = round(
        sum(1 for e in final_equities if e > initial_capital) / len(final_equities) * 100, 2
    )

    dd_5th_idx = min(int(len(max_drawdowns) * 0.95), len(max_drawdowns) - 1)
    results["worst_drawdown_5th"] = round(max_drawdowns[dd_5th_idx] * 100, 2)
    results["median_return"] = results["percentiles"].get("p50_return_pct")

    return results, None


# ---------------------------------------------------------------------------
# Prop firm simulation
# ---------------------------------------------------------------------------

def simulate_prop_firm(trade_returns, prop_firm_config, account_size):
    """Simulate prop firm rules against a sequence of trade returns."""
    if not prop_firm_config or not trade_returns:
        return None

    max_drawdown = prop_firm_config.get("max_drawdown", float("inf"))
    daily_loss_limit = prop_firm_config.get("daily_loss_limit")
    profit_target = prop_firm_config.get("profit_target", float("inf"))
    consistency_pct = prop_firm_config.get("consistency_pct")

    result = {
        "passed_eval": False,
        "blown_account": False,
        "days_to_pass": None,
        "final_pnl": 0,
        "max_drawdown_hit": 0,
        "consistency_passed": True,
        "daily_limit_violations": 0,
    }

    equity = account_size
    high_water = account_size
    daily_pnl = 0
    total_profit = 0
    trading_day = 0
    day_pnls = []

    for i, ret in enumerate(trade_returns):
        daily_pnl += ret
        equity += ret

        # Update high water mark
        if equity > high_water:
            high_water = equity

        # Check drawdown
        drawdown = high_water - equity
        result["max_drawdown_hit"] = max(result["max_drawdown_hit"], drawdown)

        if drawdown >= max_drawdown:
            result["blown_account"] = True
            break

        # Simulate daily boundary (every N trades or just per trade for simplicity)
        # For a proper simulation we'd track days, but we approximate
        if (i + 1) % 3 == 0 or i == len(trade_returns) - 1:  # ~3 trades per day
            trading_day += 1
            day_pnls.append(daily_pnl)

            # Daily loss limit check
            if daily_loss_limit and daily_pnl < -daily_loss_limit:
                result["daily_limit_violations"] += 1

            total_profit = equity - account_size
            daily_pnl = 0

            # Check if target reached
            if total_profit >= profit_target and not result["passed_eval"]:
                result["passed_eval"] = True
                result["days_to_pass"] = trading_day

    result["final_pnl"] = round(equity - account_size, 2)

    # Consistency check
    if consistency_pct and total_profit > 0 and day_pnls:
        max_day_pnl = max(day_pnls) if day_pnls else 0
        if max_day_pnl / total_profit > consistency_pct:
            result["consistency_passed"] = False

    result["max_drawdown_hit"] = round(result["max_drawdown_hit"], 2)

    return result


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def safe_float(val, default=None):
    try:
        v = float(val)
        return round(v, 4) if not math.isnan(v) and not math.isinf(v) else default
    except (TypeError, ValueError):
        return default


def safe_int(val, default=0):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def extract_trade_returns(stats):
    """Extract individual trade returns from backtesting.py stats."""
    try:
        trades_df = stats.get("_trades")
        if trades_df is not None and hasattr(trades_df, "__len__") and len(trades_df) > 0:
            if "PnL" in trades_df.columns:
                return trades_df["PnL"].tolist()
            elif "ReturnPct" in trades_df.columns:
                return trades_df["ReturnPct"].tolist()
    except Exception:
        pass
    return []


def format_stats(stats):
    """Convert backtesting.py stats to a clean dict."""
    key_metrics = {}
    fields = [
        "Start", "End", "Duration", "Exposure Time [%]",
        "Equity Final [$]", "Equity Peak [$]", "Return [%]",
        "Buy & Hold Return [%]", "Return (Ann.) [%]",
        "Volatility (Ann.) [%]", "Sharpe Ratio", "Sortino Ratio",
        "Calmar Ratio", "Max. Drawdown [%]", "Avg. Drawdown [%]",
        "Max. Drawdown Duration", "Avg. Drawdown Duration",
        "# Trades", "Win Rate [%]", "Best Trade [%]",
        "Worst Trade [%]", "Avg. Trade [%]",
        "Max. Trade Duration", "Avg. Trade Duration",
        "Profit Factor", "Expectancy [%]", "SQN",
    ]
    for f in fields:
        val = stats.get(f)
        if val is not None:
            if isinstance(val, float):
                key_metrics[f] = safe_float(val)
            elif hasattr(val, "days"):
                key_metrics[f] = str(val)
            else:
                key_metrics[f] = val

    return key_metrics


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Backtest a trading strategy with prop firm simulation")
    parser.add_argument("--config", required=True, help="Path to strategy JSON config file")
    parser.add_argument("--prop-firm", default=None, help="Prop firm name for simulation")
    parser.add_argument("--account-size", type=float, default=50000, help="Account size (default: 50000)")
    parser.add_argument("--output-report", default=None, help="Path to save markdown report (optional)")
    args = parser.parse_args()

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "strategy": None,
        "data_info": None,
        "full_results": None,
        "in_sample": None,
        "out_of_sample": None,
        "walk_forward": None,
        "monte_carlo": None,
        "prop_firm_simulation": None,
        "gate_1_profitability": None,
        "gate_2_prop_firm": None,
        "recommendation": None,
        "error": None,
    }

    # Load config
    try:
        config_path = Path(args.config)
        if not config_path.exists():
            output["error"] = f"Config file not found: {args.config}"
            print(json.dumps(output, indent=2))
            return
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        output["error"] = f"Invalid JSON in config file: {e}"
        print(json.dumps(output, indent=2))
        return
    except Exception as e:
        output["error"] = f"Error reading config: {e}"
        print(json.dumps(output, indent=2))
        return

    output["strategy"] = {
        "name": config.get("name", "unnamed"),
        "instrument": config.get("instrument", "ES1!"),
        "timeframe": config.get("timeframe", "1h"),
        "setup": config.get("entry_rules", {}).get("setup", "unknown"),
    }

    pd, np = safe_import_pandas()
    if pd is None:
        output["error"] = "pandas/numpy not installed. Run install_deps.py first."
        print(json.dumps(output, indent=2))
        return

    BacktestClass, StrategyBase = safe_import_backtesting()
    if BacktestClass is None:
        output["error"] = "backtesting library not installed. Run install_deps.py first."
        print(json.dumps(output, indent=2))
        return

    # Fetch data
    instrument = config.get("instrument", "ES1!")
    exchange = config.get("exchange", "CME")
    timeframe = config.get("timeframe", "1h")
    data_range = config.get("data_range", {})
    start_date = data_range.get("start")
    end_date = data_range.get("end")

    data, fetch_err = fetch_data(instrument, exchange, timeframe, start_date, end_date)
    if fetch_err:
        output["error"] = fetch_err
        print(json.dumps(output, indent=2))
        return

    output["data_info"] = {
        "bars": len(data),
        "start": str(data.index[0]),
        "end": str(data.index[-1]),
        "instrument": instrument,
        "exchange": exchange,
        "timeframe": timeframe,
    }

    # Build strategy
    StrategyClass = build_strategy_class(config, data, StrategyBase)
    cash = args.account_size
    commission = config.get("commission", 0.002)

    # --- Full backtest ---
    try:
        bt = BacktestClass(data, StrategyClass, cash=cash, commission=commission)
        stats = bt.run()
        output["full_results"] = format_stats(stats)
        trade_returns = extract_trade_returns(stats)
    except Exception as e:
        output["error"] = f"Backtest execution error: {e}"
        print(json.dumps(output, indent=2))
        return

    # --- In-sample / Out-of-sample split ---
    in_sample_pct = config.get("in_sample_pct", 70) / 100.0
    split_idx = int(len(data) * in_sample_pct)

    if split_idx > 50 and len(data) - split_idx > 20:
        in_sample_data = data.iloc[:split_idx]
        out_sample_data = data.iloc[split_idx:]

        try:
            bt_is = BacktestClass(in_sample_data, StrategyClass, cash=cash, commission=commission)
            is_stats = bt_is.run()
            output["in_sample"] = format_stats(is_stats)
        except Exception as e:
            output["in_sample"] = {"error": str(e)}

        try:
            bt_os = BacktestClass(out_sample_data, StrategyClass, cash=cash, commission=commission)
            os_stats = bt_os.run()
            output["out_of_sample"] = format_stats(os_stats)
        except Exception as e:
            output["out_of_sample"] = {"error": str(e)}

    # --- Walk-forward analysis ---
    wf_config = config.get("walk_forward_windows", {})
    opt_months = wf_config.get("optimize_months", 3)
    test_months = wf_config.get("test_months", 1)

    wf_results, wf_err = walk_forward_analysis(
        data, config, BacktestClass, StrategyClass, cash, commission,
        opt_months, test_months,
    )
    if wf_err:
        output["walk_forward"] = {"error": wf_err}
    else:
        # Compute Walk-Forward Efficiency (WFE)
        wfe_values = []
        for wr in wf_results:
            opt_ret = wr.get("opt_return_pct")
            test_ret = wr.get("test_return_pct")
            if opt_ret and test_ret and opt_ret != 0:
                wfe_values.append(test_ret / opt_ret)

        output["walk_forward"] = {
            "windows": wf_results,
            "total_windows": len(wf_results),
            "avg_wfe": round(sum(wfe_values) / len(wfe_values), 4) if wfe_values else None,
            "profitable_windows": sum(1 for w in wf_results if (w.get("test_return_pct") or 0) > 0),
        }

    # --- Monte Carlo ---
    mc_runs = config.get("monte_carlo_runs", 1000)
    if trade_returns:
        mc_results, mc_err = monte_carlo_simulation(trade_returns, cash, mc_runs)
        if mc_err:
            output["monte_carlo"] = {"error": mc_err}
        else:
            output["monte_carlo"] = mc_results
    else:
        output["monte_carlo"] = {"error": "No trade returns available for Monte Carlo."}

    # --- Prop firm simulation ---
    if args.prop_firm:
        profiles_path = Path(__file__).resolve().parent.parent / "assets" / "prop-firm-profiles.json"
        try:
            with open(profiles_path, "r") as f:
                profiles = json.load(f)

            firm_key = args.prop_firm.lower().replace(" ", "").replace("-", "")
            firm_data = profiles.get(firm_key, {})
            if not firm_data:
                for k, v in profiles.items():
                    if k.startswith("_"):
                        continue
                    if firm_key in k.lower():
                        firm_data = v
                        break

            if firm_data:
                # Find matching account size
                acct_key = str(int(args.account_size / 1000)) + "k"
                acct = firm_data.get("accounts", {}).get(acct_key, {})

                pf_config = {
                    "max_drawdown": acct.get("max_drawdown") if isinstance(acct.get("max_drawdown"), (int, float)) else 3000,
                    "daily_loss_limit": acct.get("daily_loss_limit"),
                    "profit_target": acct.get("profit_target") if isinstance(acct.get("profit_target"), (int, float)) else 6000,
                    "consistency_pct": None,
                }

                cr = firm_data.get("consistency_rule", {})
                funded_pct = cr.get("funded")
                if isinstance(funded_pct, (int, float)):
                    pf_config["consistency_pct"] = funded_pct

                # Run multiple simulations with shuffled trade orders
                sim_results = []
                for _ in range(100):
                    shuffled = list(trade_returns)
                    random.shuffle(shuffled)
                    sim = simulate_prop_firm(shuffled, pf_config, args.account_size)
                    if sim:
                        sim_results.append(sim)

                if sim_results:
                    pass_count = sum(1 for s in sim_results if s["passed_eval"])
                    blow_count = sum(1 for s in sim_results if s["blown_account"])
                    consist_pass = sum(1 for s in sim_results if s["consistency_passed"])

                    output["prop_firm_simulation"] = {
                        "firm": firm_data.get("name", args.prop_firm),
                        "account_size": args.account_size,
                        "simulations": len(sim_results),
                        "eval_pass_rate": round(pass_count / len(sim_results) * 100, 2),
                        "account_blow_rate": round(blow_count / len(sim_results) * 100, 2),
                        "consistency_pass_rate": round(consist_pass / len(sim_results) * 100, 2),
                        "avg_days_to_pass": round(
                            sum(s["days_to_pass"] for s in sim_results if s["days_to_pass"]) /
                            max(1, pass_count), 1
                        ) if pass_count > 0 else None,
                        "avg_max_drawdown": round(
                            sum(s["max_drawdown_hit"] for s in sim_results) / len(sim_results), 2
                        ),
                    }
        except Exception as e:
            output["prop_firm_simulation"] = {"error": str(e)}

    # --- Gate evaluations ---
    # Gate 1: Profitability
    full = output["full_results"] or {}
    pf = safe_float(full.get("Profit Factor"), 0)
    sharpe = safe_float(full.get("Sharpe Ratio"), 0)
    wfe = output.get("walk_forward", {}).get("avg_wfe")
    mc = output.get("monte_carlo", {})
    mc_p5_profitable = (mc.get("percentiles", {}).get("p5_return_pct", -1) or -1) > 0 if isinstance(mc, dict) else False

    gate1 = {
        "profit_factor": {"value": pf, "threshold": 1.5, "passed": (pf or 0) >= 1.5},
        "sharpe_ratio": {"value": sharpe, "threshold": 1.0, "passed": (sharpe or 0) >= 1.0},
        "walk_forward_efficiency": {"value": wfe, "threshold": 0.5, "passed": (wfe or 0) >= 0.5 if wfe is not None else None},
        "monte_carlo_5th_pct": {"profitable": mc_p5_profitable},
        "overall": False,
    }
    gate1_checks = [gate1["profit_factor"]["passed"], gate1["sharpe_ratio"]["passed"], mc_p5_profitable]
    if wfe is not None:
        gate1_checks.append(gate1["walk_forward_efficiency"]["passed"])
    gate1["overall"] = all(c for c in gate1_checks if c is not None)
    output["gate_1_profitability"] = gate1

    # Gate 2: Prop Firm Viability
    if output.get("prop_firm_simulation") and "error" not in output["prop_firm_simulation"]:
        pfs = output["prop_firm_simulation"]
        gate2 = {
            "eval_pass_rate": {"value": pfs["eval_pass_rate"], "threshold": 70, "passed": pfs["eval_pass_rate"] >= 70},
            "account_blow_rate": {"value": pfs["account_blow_rate"], "threshold": 20, "passed": pfs["account_blow_rate"] <= 20},
            "consistency_pass": {"value": pfs["consistency_pass_rate"], "passed": pfs["consistency_pass_rate"] >= 80},
            "overall": False,
        }
        gate2["overall"] = all([gate2["eval_pass_rate"]["passed"], gate2["account_blow_rate"]["passed"], gate2["consistency_pass"]["passed"]])
        output["gate_2_prop_firm"] = gate2
    else:
        output["gate_2_prop_firm"] = {"overall": None, "note": "No prop firm simulation run."}

    # --- Recommendation ---
    g1_pass = gate1.get("overall", False)
    g2_pass = output.get("gate_2_prop_firm", {}).get("overall")

    if g1_pass and g2_pass:
        output["recommendation"] = "GO - Strategy passes both profitability and prop firm viability gates. Proceed to forward testing."
    elif g1_pass and g2_pass is None:
        output["recommendation"] = "CONDITIONAL GO - Strategy is profitable but no prop firm simulation was run. Consider testing with --prop-firm."
    elif g1_pass and not g2_pass:
        output["recommendation"] = "NO GO (PROP FIRM) - Strategy is profitable but fails prop firm viability. Adjust position sizing, drawdown management, or target/stop levels."
    else:
        output["recommendation"] = "NO GO - Strategy fails profitability gate. Reconsider entry/exit rules, timeframe, or instrument."

    # --- Save report ---
    if args.output_report:
        try:
            report = generate_markdown_report(output, config)
            report_path = Path(args.output_report)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w") as f:
                f.write(report)
            output["report_saved"] = str(report_path)
        except Exception as e:
            output["report_save_error"] = str(e)

    print(json.dumps(output, indent=2))


def generate_markdown_report(output, config):
    """Generate a markdown backtest report."""
    lines = []
    lines.append(f"# Backtest Report: {config.get('name', 'unnamed')}")
    lines.append(f"**Date:** {output['timestamp']}")
    lines.append(f"**Instrument:** {config.get('instrument')}")
    lines.append(f"**Timeframe:** {config.get('timeframe')}")
    lines.append(f"**Setup:** {config.get('entry_rules', {}).get('setup', 'N/A')}")
    lines.append("")

    # Full results
    full = output.get("full_results", {})
    if full:
        lines.append("## Full Backtest Results")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        for k, v in full.items():
            lines.append(f"| {k} | {v} |")
        lines.append("")

    # Walk forward
    wf = output.get("walk_forward", {})
    if wf and "windows" in wf:
        lines.append("## Walk-Forward Analysis")
        lines.append(f"- Total windows: {wf.get('total_windows')}")
        lines.append(f"- Average WFE: {wf.get('avg_wfe')}")
        lines.append(f"- Profitable windows: {wf.get('profitable_windows')}/{wf.get('total_windows')}")
        lines.append("")

    # Monte Carlo
    mc = output.get("monte_carlo", {})
    if mc and "percentiles" in mc:
        lines.append("## Monte Carlo Simulation")
        lines.append(f"- Runs: {mc.get('runs')}")
        lines.append(f"- Probability profitable: {mc.get('probability_profitable')}%")
        lines.append(f"- Median return: {mc.get('median_return')}%")
        lines.append(f"- 5th percentile drawdown: {mc.get('worst_drawdown_5th')}%")
        lines.append("")

    # Prop firm
    pfs = output.get("prop_firm_simulation", {})
    if pfs and "eval_pass_rate" in pfs:
        lines.append("## Prop Firm Simulation")
        lines.append(f"- Firm: {pfs.get('firm')}")
        lines.append(f"- Eval pass rate: {pfs.get('eval_pass_rate')}%")
        lines.append(f"- Account blow rate: {pfs.get('account_blow_rate')}%")
        lines.append(f"- Consistency pass rate: {pfs.get('consistency_pass_rate')}%")
        lines.append("")

    # Gates
    lines.append("## Gate Evaluation")
    g1 = output.get("gate_1_profitability", {})
    lines.append(f"- **Gate 1 (Profitability):** {'PASS' if g1.get('overall') else 'FAIL'}")
    g2 = output.get("gate_2_prop_firm", {})
    lines.append(f"- **Gate 2 (Prop Firm):** {'PASS' if g2.get('overall') else 'FAIL' if g2.get('overall') is False else 'N/A'}")
    lines.append("")

    lines.append(f"## Recommendation")
    lines.append(f"**{output.get('recommendation', 'N/A')}**")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
