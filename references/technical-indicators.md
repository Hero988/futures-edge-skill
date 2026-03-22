# Technical Indicators Reference
last_verified: 2026-03-22

## Overview

This reference covers the primary technical indicators used in futures trading. Each indicator includes calculation, interpretation, actionable signals, and common pitfalls. Indicators are tools, not signals by themselves -- always combine with price action and context.

---

## VWAP (Volume Weighted Average Price)

### Calculation
VWAP = Cumulative(Price x Volume) / Cumulative(Volume), reset each session.

### Standard Deviation Bands
- **+1 SD / -1 SD**: First standard deviation. Price spends ~68% of time here in a balanced day.
- **+2 SD / -2 SD**: Second standard deviation. Extreme levels, often act as reversal zones.
- **+3 SD / -3 SD**: Rarely reached. Strong mean reversion expected.

### As Bias Filter
- **Price above VWAP**: Bullish intraday bias. Prefer longs.
- **Price below VWAP**: Bearish intraday bias. Prefer shorts.
- **Price at VWAP**: Neutral/contested. Wait for directional commitment.

### Session VWAP vs Anchored VWAP
- **Session VWAP**: Resets daily at RTH open (or Globex open). Standard use.
- **Anchored VWAP**: Anchored to a specific event (earnings, swing low, FOMC). Shows avg price since that event.
- **Developing VWAP**: Previous day's closing VWAP often acts as support/resistance the next day.

### Trading VWAP
- In a trending day: trade bounces off VWAP in the trend direction. Price touches VWAP and holds = entry.
- In a ranging day: fade moves at +/- 2 SD bands back toward VWAP.
- VWAP cross: When price decisively crosses VWAP with volume, bias shifts. Wait for retest to enter.

---

## EMA (Exponential Moving Average) Systems

### Key EMAs
| EMA    | Use                | Timeframe       |
|--------|--------------------|-----------------|
| 9 EMA  | Fast entry/exit    | 5M, 15M         |
| 21 EMA | Short-term trend   | 15M, 1H         |
| 50 EMA | Swing trend        | 1H, 4H          |
| 200 EMA| Major trend filter | 1H, 4H, Daily   |

### Crossover Signals
- **9/21 EMA Cross**: Fast signal for entries. Bullish = 9 crosses above 21. Bearish = 9 crosses below 21. Works well in Kill Zones.
- **50/200 EMA Cross (Golden/Death Cross)**: Slow signal for bias. Golden Cross (50 above 200) = bullish regime. Death Cross (50 below 200) = bearish regime. Use on 1H or higher.

### EMA as Dynamic Support/Resistance
- In an uptrend: price pulls back to 9 or 21 EMA and bounces = continuation entry
- In a strong uptrend: price respects 9 EMA on pullbacks (shallow retracements)
- In a moderate uptrend: price pulls back to 21 or 50 EMA
- Losing the 50 EMA on the 1H chart often signals a deeper correction

### EMA Stacking
- **Bullish stack**: 9 > 21 > 50 > 200 (all aligned). Strongest bullish signal.
- **Bearish stack**: 9 < 21 < 50 < 200. Strongest bearish signal.
- **Tangled EMAs**: No clear order. Choppy/ranging market. Reduce trading or sit out.

---

## RSI (Relative Strength Index)

### Standard Settings
- Period: 14
- Overbought: > 70
- Oversold: < 30
- Midline: 50

### Interpretation
- **Above 70**: Overbought. Does NOT mean "sell immediately." In strong trends, RSI can stay above 70 for extended periods. Overbought in a range = fade. Overbought in a trend = wait for divergence.
- **Below 30**: Oversold. Same logic inverted.
- **Crossing 50**: Trend bias change. RSI crossing above 50 = bullish shift. Below 50 = bearish shift.

### RSI Divergence
- **Regular Bullish Divergence**: Price makes a lower low, RSI makes a higher low. Signals weakening selling pressure. Potential reversal up.
- **Regular Bearish Divergence**: Price makes a higher high, RSI makes a lower high. Signals weakening buying pressure. Potential reversal down.
- **Hidden Bullish Divergence**: Price makes a higher low, RSI makes a lower low. Signals trend continuation in an uptrend.
- **Hidden Bearish Divergence**: Price makes a lower high, RSI makes a higher high. Signals trend continuation in a downtrend.

### RSI Tips
- Divergence is a warning, not a signal. Combine with price action (CHoCH, OB) for entries.
- On 5M charts, use RSI(9) for faster signals. On Daily, stick with RSI(14).
- In strong trends, 40-50 zone acts as "oversold" (uptrend) or 50-60 acts as "overbought" (downtrend).

---

## MACD (Moving Average Convergence Divergence)

### Standard Settings
- Fast: 12, Slow: 26, Signal: 9
- Intraday alternative: Fast: 6, Slow: 13, Signal: 5 (more responsive for scalping)

### Components
- **MACD Line**: 12 EMA minus 26 EMA. Direction = momentum.
- **Signal Line**: 9 EMA of the MACD line. Crossovers = entry/exit signals.
- **Histogram**: MACD minus Signal. Expanding = strengthening momentum. Contracting = weakening.

### Signals
- **Signal Line Crossover**: MACD crosses above signal = bullish. Below = bearish. Most common signal.
- **Zero Line Cross**: MACD crosses above zero = bullish regime. Below zero = bearish. Slower but more reliable.
- **Histogram Divergence**: Histogram making lower peaks while price makes higher highs = bearish divergence.

### MACD Divergence
- Same logic as RSI divergence but using the MACD line or histogram
- MACD divergence on higher timeframes (4H, Daily) is very reliable
- Double divergence (two consecutive divergences) = very strong reversal signal

### MACD Pitfalls
- Lagging indicator: signals come after the move starts
- Produces many false signals in ranging markets
- Best used as confirmation, not primary signal

---

## Bollinger Bands

### Standard Settings
- Period: 20 (20 SMA center line)
- Width: 2 standard deviations

### Bollinger Squeeze
- Bands narrow (low volatility) = price is coiling
- Expect a breakout/expansion in either direction
- Use other indicators (VWAP, trend) to determine direction
- Squeeze duration: longer squeeze = more powerful breakout

### Band Walk
- In strong trends, price "walks" along the upper or lower band
- Upper band walk: price stays between upper band and 20 SMA. Do NOT fade this.
- Lower band walk: price stays between lower band and 20 SMA. Do NOT buy dips into this.

### Mean Reversion (Range Markets)
- In a range: price touching upper band = short opportunity (target: 20 SMA or lower band)
- Price touching lower band = long opportunity (target: 20 SMA or upper band)
- Only use mean reversion when market is clearly ranging (flat 20 SMA, no band walk)

### Bollinger Band Width
- BBW = (Upper - Lower) / Middle
- Historically low BBW = squeeze imminent
- Compare current BBW to last 100 periods to gauge relative volatility

---

## ATR (Average True Range)

### Calculation
- True Range = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
- ATR = 14-period average of True Range

### Use for Stop Placement
- **Tight stop**: 1.5x ATR from entry
- **Standard stop**: 2x ATR from entry
- **Wide stop (swing)**: 3x ATR from entry
- Example: ES ATR(14) on 15M = 4 points. Standard stop = 8 points from entry.

### Use for Position Sizing
- Higher ATR = higher volatility = fewer contracts for same dollar risk
- Position Size = Risk_Dollars / (ATR_Multiple x ATR x Point_Value)

### Regime Detection
- **High ATR (above 20-period average)**: Volatile market. Widen stops, reduce size, expect fast moves.
- **Low ATR (below 20-period average)**: Quiet market. Tighten stops, expect a breakout soon.
- **ATR expansion**: Breakout in progress. Get on the right side of the move.
- **ATR contraction**: Move is exhausting. Consider taking profits.

---

## Volume Profile

### Key Levels
- **POC (Point of Control)**: Price with the most traded volume. Acts as a magnet. Price tends to gravitate toward POC.
- **Value Area High (VAH)**: Upper boundary of the 70% volume zone. Resistance in downtrends, support if reclaimed.
- **Value Area Low (VAL)**: Lower boundary of the 70% volume zone. Support in uptrends, resistance if lost.
- **High Volume Nodes (HVN)**: Areas of high volume. Price tends to consolidate here. Act as support/resistance.
- **Low Volume Nodes (LVN)**: Areas of low volume. Price moves through these quickly. Poor support/resistance. Use as breakout acceleration zones.

### Naked POC
- A POC from a prior session that has not been revisited
- Price has a strong tendency to return to naked POCs
- Mark prior session POCs that remain untouched as targets

### Trading Volume Profile
- **Opening within Value Area**: Expect rotation between VAH and VAL (range day)
- **Opening outside Value Area**: Expect trend day or value area migration
- **Breakout above VAH with acceptance**: Bullish, target next HVN or prior naked POC
- **Breakdown below VAL with acceptance**: Bearish, target next HVN or prior naked POC

---

## Market Profile (TPO)

### TPO Letters
- Each 30-minute period is assigned a letter (A, B, C, etc.)
- Letters stack to show where price spent the most time
- Wide TPO distribution = acceptance (fair value)
- Narrow TPO = rejection (price moved through quickly)

### Initial Balance (IB)
- The range of the first hour of RTH trading (A + B periods)
- IB range predicts day type:
  - Wide IB (> 1.5x avg): Likely range/rotation day
  - Narrow IB (< 0.5x avg): Likely trend/breakout day
  - Normal IB: Could go either way, watch for IB break

### Day Types
- **Normal Day**: 85% of activity within IB. Low directional conviction.
- **Normal Variation**: IB extended on one side, 1x IB range. Moderate trend.
- **Trend Day**: IB extended on one side, > 2x IB range. Strong directional move. Rare (15% of days). Go with the trend, do NOT fade.
- **Neutral Day**: IB extended on both sides. Choppy. Avoid or fade extremes.
- **Double Distribution**: Two distinct areas of value. Gap or news-driven. Trade between the distributions or wait for acceptance.

---

## Delta / Cumulative Delta

### Definition
- Delta = Buying Volume minus Selling Volume for a given bar
- Cumulative Delta (CD) = Running total of delta from session start

### Interpretation
- **Positive delta + price up**: Confirmed buying. Healthy uptrend.
- **Negative delta + price down**: Confirmed selling. Healthy downtrend.
- **Positive delta + price flat/down**: Absorption. Buyers being absorbed by sellers. Bearish.
- **Negative delta + price flat/up**: Absorption. Sellers being absorbed by buyers. Bullish.

### Delta Divergence
- Price making new highs + cumulative delta making lower highs = weakening buying. Expect reversal.
- Price making new lows + cumulative delta making higher lows = weakening selling. Expect reversal.
- Delta divergence is one of the most reliable short-term reversal signals.

### Breakout Confirmation
- A true breakout should have delta confirmation (positive delta on upside break, negative on downside break)
- Breakout with flat or opposing delta = likely false breakout. Fade it.
