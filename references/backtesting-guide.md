# Backtesting Guide Reference
last_verified: 2026-03-22

## Overview

Backtesting is the process of applying a trading strategy to historical data to evaluate its performance. Done correctly, it quantifies your edge before risking real capital. Done incorrectly, it gives false confidence and leads to real losses.

---

## Why Backtest

### The Case for Backtesting
- **Validates edge**: Proves (or disproves) that your strategy has positive expected value over a meaningful sample
- **Quantifies expectations**: You know your expected win rate, profit factor, max drawdown, and average R BEFORE you trade live
- **Builds confidence**: When drawdowns happen live (and they will), you have data showing that the strategy recovers
- **Identifies weaknesses**: Reveals which market conditions your strategy struggles in (trending vs ranging, high vol vs low vol)
- **Prop firm simulation**: Can simulate whether your strategy would survive prop firm drawdown rules, consistency rules, and session restrictions

### What Backtesting Cannot Do
- Guarantee future results (markets evolve)
- Account for execution psychology (slippage, hesitation, emotion)
- Perfectly replicate live fills (especially in fast markets)
- Replace forward testing (backtesting is necessary but not sufficient)

---

## Statistical Requirements

### Minimum Sample Sizes
| Confidence Level | Required Trades | Use Case                          |
|------------------|----------------|-----------------------------------|
| Rough estimate   | 30 trades      | Quick initial viability check      |
| Moderate confidence | 100 trades  | Minimum for any real conclusions   |
| High confidence (95%) | 385 trades | Statistically significant results |
| Publication quality | 1000+ trades | Robust across conditions           |

### Why 100 Trades is the Minimum
- With fewer than 100 trades, random variance dominates results
- A 60% win rate strategy can easily show 45% or 75% over 30 trades by pure chance
- At 100 trades, the confidence interval narrows enough to be useful
- At 385 trades, a 60% observed win rate means the true win rate is between 55-65% with 95% confidence

### Data Requirements
- **Minimum 2 years of data** to capture different market regimes
- **Ideally 3-5 years** to include: bull markets, bear markets, high and low volatility, black swan events
- **Multiple instruments**: If strategy is designed for ES, also test on NQ and YM to validate
- **Tick or 1-minute data** for intraday strategies (5M or higher bars miss important price action)

---

## Data Splitting: In-Sample vs Out-of-Sample

### The Principle
- **In-sample (IS)**: Data used to develop and optimize the strategy (70% of total data)
- **Out-of-sample (OOS)**: Data reserved for validation, never seen during development (30% of total data)
- The OOS test is the true test of strategy robustness

### How to Split
```
Total data: Jan 2022 - Dec 2025 (4 years)
In-sample:  Jan 2022 - Oct 2024 (70% = ~2.8 years)
Out-of-sample: Nov 2024 - Dec 2025 (30% = ~1.2 years)
```

### Expected Degradation
- A well-designed strategy should retain **50-75% of IS performance** on OOS data
- If OOS performance is > 90% of IS: Possible look-ahead bias or the strategy is genuinely robust
- If OOS performance is < 50% of IS: Strategy is likely overfit to IS data
- If OOS performance is negative: Strategy has no edge. Discard or fundamentally redesign.

### Rules
- **NEVER optimize on OOS data**. Once you look at OOS results and then adjust the strategy, the OOS data is contaminated.
- **Use OOS data exactly once**. It is a one-shot test. If you fail, go back to IS data, redesign, and create a NEW OOS split.
- **Time-based splits only**. Do not randomly sample. Markets have temporal structure (trends, regimes) that random sampling destroys.

---

## Walk-Forward Analysis (WFA)

### What It Is
Rolling windows of optimization and testing that simulate how you would actually use the strategy in real time.

### How It Works
1. Optimize on window 1 (e.g., months 1-6)
2. Test on window 2 (e.g., months 7-8) using the optimized parameters
3. Slide forward: Optimize on months 3-8, test on months 9-10
4. Repeat until all data is consumed
5. Aggregate all test-window results for the final performance metrics

### Walk-Forward Efficiency (WFE)
```
WFE = Average OOS Return / Average IS Return
```
- **WFE > 0.50**: Strategy is robust. Parameters are stable.
- **WFE 0.30 - 0.50**: Marginal. Strategy may work but is sensitive to parameter changes.
- **WFE < 0.30**: Strategy is overfit. Parameters are unstable. Discard or simplify.

### Window Sizing
- IS window: 6-12 months for intraday strategies
- OOS window: 1-3 months
- Overlap: 50% overlap between consecutive IS windows is common
- Total: Need at least 5-6 complete walk-forward cycles for meaningful WFE

---

## Monte Carlo Simulation

### What It Is
Randomly reshuffle the order of your backtest trades thousands of times to understand the range of possible outcomes from the same edge.

### Why It Matters
- Your backtest produced ONE specific sequence of trades. That exact sequence will never repeat.
- Monte Carlo shows you the distribution of outcomes: best case, worst case, and everything in between.
- Critical for understanding realistic drawdown expectations.

### How to Run
1. Take your backtest trade results (list of R-multiples or P&L per trade)
2. Randomly reshuffle the order 1,000-10,000 times
3. For each shuffle, calculate: total return, max drawdown, consecutive losses, Sharpe ratio
4. Build distributions for each metric
5. Use the 5th percentile (worst 5%) as your planning baseline

### Key Outputs
- **95th percentile max drawdown**: Plan for this, not the backtest max DD. If your backtest max DD was $2,000, Monte Carlo 95th percentile might be $3,500.
- **Probability of ruin**: What % of simulations result in account failure (hitting max DD)?
- **Expected return range**: 5th to 95th percentile of total returns
- **Consecutive loss streaks**: Maximum expected losing streak at 95% confidence

### Rule of Thumb
- If probability of ruin > 5% under prop firm drawdown rules: strategy is too risky for that firm. Reduce position size or improve edge.

---

## Common Backtesting Pitfalls

### Overfitting
- **What**: Too many parameters tuned to historical data. The strategy fits the past perfectly but fails on new data.
- **Signs**: Exceptional IS performance, terrible OOS performance. Strategy has 5+ adjustable parameters. Small parameter changes cause large performance swings.
- **Prevention**: Keep parameter count low (3-5 max). Use walk-forward analysis. Test on multiple instruments.

### Look-Ahead Bias
- **What**: Using information that would not have been available at the time of the trade.
- **Examples**: Using the daily close to make a decision at 10 AM. Using next candle's high to set entry. Knowing earnings results before they happen.
- **Prevention**: Ensure every decision point uses only data available at or before that bar's timestamp. Use bar-by-bar simulation, not vectorized calculations.

### Survivorship Bias
- **What**: Only testing on instruments that survived to the present. Failed/delisted instruments are excluded.
- **Relevance to futures**: Less relevant (major contracts persist) but applies to equity index composition. The current S&P 500 members are not the same as 5 years ago.
- **Prevention**: Use point-in-time index composition data if applicable.

### Ignoring Transaction Costs
- **What**: Backtesting without commissions, slippage, and fees.
- **Impact**: A strategy making $2 per trade gross becomes -$3.50 per trade after costs.
- **Prevention**: Always include realistic costs (see Slippage Modeling section below).

### Cherry-Picking Start Dates
- **What**: Starting the backtest at a favorable point (e.g., right before a trending period for a trend-following strategy).
- **Prevention**: Test over the full available data range. Use multiple start dates. Walk-forward analysis inherently addresses this.

---

## Prop Firm Simulation

### What to Simulate
When backtesting for prop firm trading, standard metrics are not enough. You must also simulate:

1. **Drawdown rules**: Apply the firm's specific drawdown type (trailing vs EOD vs static) to each trade sequence
2. **Daily loss limits**: If the firm has a DLL, check if any single day exceeds it
3. **Consistency rules**: Check if any single day exceeds the consistency limit (30-50% of total profit)
4. **Session restrictions**: Only count trades taken within the firm's allowed hours
5. **News blackouts**: Remove trades taken within the blackout window around major releases
6. **Close-by time**: Ensure no trades are held past the firm's cutoff time
7. **Contract limits**: Cap position size at the firm's maximum contracts

### Pass Rate Analysis
- Run Monte Carlo simulation with prop firm rules applied
- Calculate: What % of simulations pass the evaluation?
- Calculate: What % of simulations survive the funded phase for 6 months?
- Target: > 60% pass rate on evaluation, > 40% 6-month survival on funded

---

## Key Performance Metrics

| Metric            | Formula / Definition                        | Target       | Notes                         |
|-------------------|---------------------------------------------|-------------|-------------------------------|
| Win Rate          | Winning Trades / Total Trades               | > 50%       | Higher is better but not everything |
| Profit Factor     | Gross Profit / Gross Loss                   | > 1.5       | 2.0+ is excellent             |
| Sharpe Ratio      | Mean Return / Std Dev of Returns (annualized)| > 1.0      | 2.0+ is excellent             |
| Sortino Ratio     | Mean Return / Downside Deviation            | > 2.0       | Better than Sharpe for asymmetric returns |
| Max Drawdown      | Largest peak-to-trough decline              | < 15%       | Lower is better               |
| Calmar Ratio      | Annual Return / Max Drawdown                | > 1.0       | 2.0+ is excellent             |
| Expectancy        | (WinRate x AvgWin) - (LossRate x AvgLoss)  | > $0        | Must be positive              |
| Average R         | Mean R-multiple across all trades           | > 0.3R      | Positive = edge exists         |
| Recovery Factor   | Net Profit / Max Drawdown                   | > 3.0       | How efficiently DD is recovered |

---

## Libraries and Tools

### Python Libraries
- **backtesting.py**: Lightweight strategy backtesting engine. Event-driven, supports custom indicators. Good for rapid prototyping.
- **smartmoneyconcepts** (PyPI): Automated detection of ICT concepts (order blocks, FVGs, BOS, CHoCH, liquidity sweeps) from OHLCV data. Essential for ICT strategy backtesting.
- **tvdatafeed**: Fetch historical data from TradingView. Free, supports all futures contracts. Use for data collection.
- **vectorbt**: High-performance vectorized backtesting. Faster than event-driven for large datasets. Good for parameter optimization.
- **pandas / numpy**: Data manipulation and statistical analysis.
- **scipy.stats**: Statistical tests (t-test for edge significance, chi-square for win rate).
- **matplotlib / plotly**: Visualization of equity curves, drawdowns, trade distributions.

### Data Sources
- **TradingView (via tvdatafeed)**: Free, reliable, supports continuous contracts
- **Databento**: Professional-grade tick data, CME direct feed, paid but high quality
- **Polygon.io**: Aggregated futures data, reasonable pricing
- **CQG / Rithmic**: Direct exchange data (if you have a broker connection)

---

## Slippage and Commission Modeling

### Slippage Assumptions
| Contract | Slippage per Side | Notes                                    |
|----------|------------------|------------------------------------------|
| ES / MES | 1 tick           | Highly liquid, minimal slippage          |
| NQ / MNQ | 1-2 ticks        | Slightly wider spreads than ES           |
| YM / MYM | 1 tick           | Liquid, tight spreads                    |
| RTY / M2K| 2 ticks          | Less liquid, wider spreads               |
| CL / MCL | 1-2 ticks        | Liquid during RTH, wider overnight       |
| GC / MGC | 1-2 ticks        | Moderate liquidity                       |

### Commission Assumptions
- **Standard contracts**: $5.50 round-trip per contract (conservative estimate including exchange fees)
- **Micro contracts**: $1.50 round-trip per contract
- **Prop firm accounts**: Often lower or included in platform fees, but model at standard rates for conservative estimates

### Total Cost per Trade
```
Total Cost = (Entry Slippage x Tick Value) + (Exit Slippage x Tick Value) + Commission
```
Example for ES: (1 x $12.50) + (1 x $12.50) + $5.50 = **$30.50 per round-trip per contract**

### Impact on Strategy
- If average gross profit per trade is $100 and cost is $30.50, net is $69.50 (30% reduction)
- High-frequency strategies (many trades, small targets) are most impacted by costs
- Always calculate: "What is the breakeven win rate after costs?" If it is > 55%, the strategy needs a strong edge.
