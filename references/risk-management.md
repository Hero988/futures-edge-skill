# Risk Management Reference
last_verified: 2026-03-22

## Overview

Risk management is the single most important factor in long-term trading survival. Every concept here is non-negotiable. A mediocre strategy with excellent risk management will outperform a great strategy with poor risk management every time.

---

## Core Position Sizing Formula

```
Position_Size (contracts) = (Account_Balance x Risk_Percent) / (Stop_Distance_Ticks x Tick_Value)
```

### Variables
- **Account_Balance**: Current account equity (not starting balance)
- **Risk_Percent**: Percentage of account risked per trade (typically 0.5% - 2%)
- **Stop_Distance_Ticks**: Distance from entry to stop loss, measured in ticks
- **Tick_Value**: Dollar value of one tick for the specific contract

### Worked Examples

#### Example 1: ES with 10-tick stop, 1% risk on $50,000 account
- Risk Dollars = $50,000 x 0.01 = $500
- Stop Distance = 10 ticks
- ES Tick Value = $12.50
- Stop Cost per Contract = 10 x $12.50 = $125
- Position Size = $500 / $125 = **4 contracts**

#### Example 2: NQ with 20-tick stop, 1% risk on $50,000 account
- Risk Dollars = $50,000 x 0.01 = $500
- Stop Distance = 20 ticks
- NQ Tick Value = $5.00
- Stop Cost per Contract = 20 x $5.00 = $100
- Position Size = $500 / $100 = **5 contracts**

#### Example 3: CL with 15-tick stop, 1% risk on $50,000 account
- Risk Dollars = $50,000 x 0.01 = $500
- Stop Distance = 15 ticks
- CL Tick Value = $10.00
- Stop Cost per Contract = 15 x $10.00 = $150
- Position Size = $500 / $150 = **3 contracts** (round down from 3.33)

#### Example 4: MES with 10-tick stop, 1% risk on $50,000 account
- Risk Dollars = $50,000 x 0.01 = $500
- Stop Distance = 10 ticks
- MES Tick Value = $1.25
- Stop Cost per Contract = 10 x $1.25 = $12.50
- Position Size = $500 / $12.50 = **40 micro contracts**

### Key Rule
**Always round DOWN** to the nearest whole contract. Never round up.

---

## ATR-Based Stop Placement

### Formula
```
Stop_Long = Entry - (N x ATR)
Stop_Short = Entry + (N x ATR)
```

### ATR Multipliers
| Multiplier | Style       | Use Case                                    |
|------------|-------------|---------------------------------------------|
| 1.0x ATR   | Very tight  | Scalping, high win rate required             |
| 1.5x ATR   | Tight       | Intraday momentum trades                     |
| 2.0x ATR   | Standard    | Most intraday swing trades                   |
| 2.5x ATR   | Moderate    | Swing trades, noisy markets                  |
| 3.0x ATR   | Wide        | Daily timeframe swings, high conviction      |

### ATR Stop Example
- ES 15M ATR(14) = 3.5 points = 14 ticks
- Standard stop (2x) = 7 points = 28 ticks from entry
- At $12.50/tick: risk per contract = 28 x $12.50 = $350

### ATR Stop Advantages
- Adapts automatically to current volatility
- No arbitrary fixed-point stops
- Prevents being stopped out by normal market noise

---

## Structure-Based Stop Placement

### For Long Trades
1. Identify the swing low that your trade is based on
2. Place stop **1-2 ticks below the swing low wick**
3. If using an Order Block entry, stop goes 1-2 ticks below the OB wick
4. Wider structure stop = fewer contracts (maintain same dollar risk)

### For Short Trades
1. Identify the swing high that your trade is based on
2. Place stop **1-2 ticks above the swing high wick**
3. If using an Order Block entry, stop goes 1-2 ticks above the OB wick

### Structure vs ATR: Which to Use?
- Use structure stops when there is a clear, nearby swing point
- Use ATR stops when structure is far away or unclear
- **Never use both** -- pick one methodology per trade
- Structure stops are generally preferred for ICT-based setups

---

## Partial Profit Strategy

### Standard Scaling Out Plan
| Milestone | Action                          | Remaining Position |
|-----------|---------------------------------|--------------------|
| +1R       | Take 50% profit, move stop to breakeven | 50%        |
| +2R       | Take 25% profit (half of remaining)     | 25%        |
| +3R+      | Trail remaining with structure or EMA    | 25%        |

### Why Scale Out?
- Locks in profit and reduces psychological pressure
- The breakeven stop after 1R means the trade is now "free"
- The trailing 25% allows capturing large moves when they occur
- A 3R winner with this plan yields: (0.5 x 1R) + (0.25 x 2R) + (0.25 x 3R) = 1.75R average

### Breakeven Stop Rules
- Move stop to breakeven (entry price) ONLY after taking the first partial at 1R
- Add 1-2 ticks in your favor to cover commissions (true breakeven)
- Do NOT move stop to breakeven before 1R -- this reduces win rate significantly

### Trailing Stop Methods (for the final 25%)
- **EMA trail**: Trail below 9 EMA (aggressive) or 21 EMA (moderate) on your entry timeframe
- **Structure trail**: Move stop below each new higher low (longs) or above each new lower high (shorts)
- **ATR trail**: Trail at Entry + Profit - (1.5 x ATR). Recalculate each bar.

---

## Daily Loss Rules

### Hard Rules (Non-Negotiable)
- **Maximum daily loss: 2% of account**. Once reached, close all positions and stop trading for the day.
- **Maximum consecutive losing trades: 3**. After 3 losses in a row, stop trading for the day OR take a mandatory 30-minute break.
- **Single trade max risk: 1% of account**. Never risk more than 1% on any single trade.

### Soft Rules (Adjustable Based on Experience)
- After 2 losing trades: reduce position size by 50% for the rest of the day
- After reaching 1% daily loss: only take A+ setups with minimum 3:1 R:R
- If you have not found a setup by 11 AM: consider the day a no-trade day

### Daily P&L Tracking
- Track in real-time (most platforms show this)
- Include commissions and fees in your P&L
- When you hit daily loss limit, exit platform immediately. Do not "just watch."

---

## Weekly and Monthly Rules

### Weekly Rules
- **After 3 consecutive red days**: Reduce position size by 50%, only take A+ setups
- **Weekly loss limit: 4% of account**. If reached, stop trading until Monday.
- **Weekly review mandatory**: Every weekend, review all trades, identify patterns, adjust

### Monthly Rules
- **Monthly loss limit: 8% of account**. If reached, take 1 week off minimum.
- **If 3 consecutive losing weeks**: Something is fundamentally wrong. Stop live trading. Return to paper trading for 1 week to recalibrate.

---

## Correlation Management

### Highly Correlated Pairs (Treat as ONE Position)
| Pair       | Correlation | Implication                                   |
|------------|-------------|-----------------------------------------------|
| ES & NQ    | ~0.90       | Long ES + Long NQ = 2x the risk               |
| ES & YM    | ~0.95       | Nearly identical. Pick one.                    |
| ES & RTY   | ~0.75       | Somewhat correlated. Separate but aware.       |
| CL & energy stocks | ~0.70 | Moderate correlation. Partial overlap.      |
| GC & SI    | ~0.80       | Gold and silver move together most of the time |

### Rules
- Never hold simultaneous positions in highly correlated instruments unless intentionally hedging
- If long ES and long NQ: your effective risk is nearly 2x what you calculated
- If you want exposure to both ES and NQ: split your position size (e.g., 2 ES + 2 NQ instead of 4 ES + 4 NQ)

---

## Scaling Into Positions

### Rules for Adding to Winners
1. Only add after the position is **at least 1R in profit**
2. Move original stop to breakeven before adding
3. New addition gets its own stop (structure or ATR based)
4. Total portfolio risk (original + addition) must stay under 2%
5. Maximum scale-ins: 2 additions (3 entries total)

### Never Add to Losers
- Adding to a losing position is the #1 account killer
- "Averaging down" is not a strategy. It is denial with extra contracts.
- If your entry was wrong, accept the loss and look for the next setup

---

## Kill Switch Protocol

### Trigger Conditions (ANY ONE of these)
1. 3 consecutive losing trades in a single session
2. Daily loss reaches 2% of account
3. You catch yourself deviating from the trading plan
4. You feel emotional (angry, anxious, desperate, euphoric)
5. You are about to take a "revenge trade" (you can feel it)

### Kill Switch Procedure
1. **Close all open positions immediately**. No exceptions.
2. **Close the trading platform**. Not minimize -- close.
3. **Walk away for minimum 15 minutes**. Physically leave the desk.
4. **During the break**: Deep breathing, walk, drink water. Do not look at charts on your phone.
5. **After 15 minutes**: Ask yourself "Am I calm? Can I follow my rules?" If yes, return. If not, the day is over.
6. **If returning**: Reduce position size by 50% for the rest of the day. Only A+ setups.

---

## Prop Firm-Specific Risk Adjustments

### Near Drawdown Limit (Within 30% of Max Drawdown)
- Switch to micro contracts only (MES, MNQ, MCL, MGC)
- Maximum 1-2 micro contracts per trade
- Only A+ setups with minimum 3:1 R:R
- Daily loss limit: 0.5% (tighter than normal)
- Goal: Slowly recover, not swing for the fences

### Near Consistency Rule Limit
- Some firms require no single day > X% of total profit (typically 30-50%)
- If you are near this limit, STOP taking trades that could produce large winners
- Take smaller, more consistent gains
- This seems counterintuitive but violating consistency rules means losing the account

### Trailing Drawdown Awareness
- Trailing drawdown moves up with your equity high watermark
- After a big winning day, your drawdown floor has risen
- Be especially careful the day AFTER a big win (the floor is now closer)
- Calculate your current remaining drawdown room before each session

### Buffer Strategy
- Always maintain a buffer above the drawdown limit
- Target buffer: 30% of max drawdown (e.g., if max DD is $3K, maintain $900 buffer)
- If buffer shrinks below 20%, switch to micro contracts only
