# ICT (Inner Circle Trader) Methodology Reference
last_verified: 2026-03-22

## Overview

ICT methodology is a price action framework based on how institutional participants (banks, hedge funds, market makers) move price. The core premise: smart money manipulates retail liquidity to fill large orders. Understanding their footprint gives a significant edge.

---

## Order Blocks (OB)

### Definition
An order block is the **last opposing candle before a strong displacement move**. It represents the zone where institutional orders were placed.

### Bullish Order Block
- The last **bearish (down-close) candle** before a strong bullish displacement
- Price drops into the zone, then explodes upward
- Identified by: series of candles going down, then a sudden sharp move up. The last red candle before that move is the OB.

### Bearish Order Block
- The last **bullish (up-close) candle** before a strong bearish displacement
- Price rallies into the zone, then collapses downward

### How to Identify on Chart
1. Find a strong displacement move (3+ large-bodied candles in one direction)
2. Look back to the last candle that closed in the opposite direction before the move started
3. Mark the full range of that candle (open to close = body, include wicks)
4. Higher timeframe OBs are stronger (Daily > 4H > 1H > 15M)

### Entry Method
- **Standard entry**: Enter at the **50% level of the OB body** (midpoint between open and close)
- **Aggressive entry**: Enter at the top of a bullish OB (bottom of bearish OB)
- **Conservative entry**: Wait for a lower timeframe confirmation (e.g., 5M CHoCH within the OB zone)

### Stop Placement
- Place stop **1-2 ticks beyond the OB wick** (the extreme of the candle including shadows)
- If the OB is large, use the 50% body entry to improve R:R

### Invalidation Rules
- An OB is **invalidated** if price trades through the entire body AND closes beyond it
- A wick through the OB is acceptable (liquidity grab) as long as candle body does not close through
- Once invalidated, do NOT re-enter at that OB. Look for the next one.

### Quality Filters
- Best OBs have displacement immediately after (no consolidation)
- OB should be at a premium/discount zone (above/below 50% of current range)
- OB aligned with higher timeframe bias is significantly stronger

---

## Fair Value Gaps (FVG)

### Definition
A FVG is a 3-candle pattern where the wicks of candle 1 and candle 3 do not overlap, leaving a gap in price delivery.

### Bullish FVG
- Candle 1 high < Candle 3 low
- The gap between C1 high and C3 low is the FVG zone
- Price is expected to retrace into this gap before continuing higher

### Bearish FVG
- Candle 1 low > Candle 3 high
- The gap between C3 high and C1 low is the FVG zone
- Price is expected to retrace into this gap before continuing lower

### Trading FVGs
- **Entry**: At the **50% fill** of the FVG (midpoint of the gap)
- **Stop**: Beyond the opposite side of the FVG
- **Target**: Next liquidity pool or opposing FVG
- **Most powerful when**: FVG overlaps with an Order Block (OB+FVG confluence)

### FVG Fill Rules
- A "respected" FVG: price taps into it and reverses (bullish signal)
- A "filled" FVG: price trades completely through it (FVG is consumed, no longer valid)
- Consequent encroachment: price fills exactly to the 50% midpoint then reverses (strongest reaction)

---

## Liquidity

### Buy-Side Liquidity (BSL)
- Resting above **equal highs** (double/triple tops)
- Above **swing highs** (where retail places stops for shorts)
- Above **trendline highs** (where retail trail stops)
- These are targets for institutional buying algorithms

### Sell-Side Liquidity (SSL)
- Resting below **equal lows** (double/triple bottoms)
- Below **swing lows** (where retail places stops for longs)
- Below **trendline lows** (where retail trail stops)
- These are targets for institutional selling algorithms

### Liquidity Sweep Mechanics
1. Price approaches a liquidity pool (e.g., equal highs)
2. Price spikes through the level, triggering stops (the "sweep")
3. Institutions use this liquidity to fill their opposing orders
4. Price reverses sharply from the sweep level
5. Enter on the reversal, stop above the sweep wick

### Liquidity Void
- A rapid price movement that leaves unfilled orders
- Similar to FVG but on a larger scale
- Price tends to return to fill the void eventually

---

## Break of Structure (BOS)

### Definition
Price breaks a previous swing point **in the direction of the existing trend**, confirming continuation.

### Bullish BOS
- Price breaks above a previous swing high in an uptrend
- Confirms the uptrend is intact
- Look for pullbacks to order blocks after BOS for entries

### Bearish BOS
- Price breaks below a previous swing low in a downtrend
- Confirms the downtrend is intact
- Look for rallies into order blocks after BOS for short entries

### BOS Rules
- Must be a **candle body close** beyond the structure point (wicks alone do not count)
- Internal BOS (lower timeframe) has less significance than external BOS (higher timeframe)
- Multiple BOS in the same direction = strong trend, look for pullback entries only

---

## Change of Character (CHoCH)

### Definition
Price breaks a swing point **against the current trend**, signaling a potential reversal.

### Bullish CHoCH
- In a downtrend, price breaks above the **most recent lower high**
- Suggests sellers are losing control
- Look for bullish OBs to form for long entries

### Bearish CHoCH
- In an uptrend, price breaks below the **most recent higher low**
- Suggests buyers are losing control
- Look for bearish OBs to form for short entries

### CHoCH vs BOS
- BOS = with the trend = continuation signal
- CHoCH = against the trend = reversal signal
- CHoCH requires additional confirmation (OB, FVG, liquidity sweep) before entry

---

## Kill Zones (Optimal Trading Windows)

### London Kill Zone: 2:00 AM - 5:00 AM ET
- Often sets the high or low of the day
- Look for Asia range sweep into London reversal
- Best for FX futures (6E, 6B, 6J)

### New York Open Kill Zone: 8:30 AM - 11:00 AM ET
- Highest volume, most displacement
- Economic data releases at 8:30 AM create volatility
- Best for index futures (ES, NQ, YM, RTY)
- Look for London high/low to be swept

### New York PM Kill Zone: 1:30 PM - 4:00 PM ET
- Second opportunity of the day
- Often reverses or extends the NY AM move
- MOC (market on close) orders create late-day volatility after 3:30 PM

### Asia Kill Zone: 7:00 PM - 12:00 AM ET
- Lowest volume, accumulation phase
- Defines the range that London will target
- Generally avoid trading unless strong overnight catalyst

---

## Optimal Trade Entry (OTE)

### Definition
Entry in the 62%-79% Fibonacci retracement zone of the most recent swing.

### How to Use
1. Identify a completed impulse move (swing low to swing high, or vice versa)
2. Draw Fibonacci retracement from swing start to swing end
3. The OTE zone is between the **0.618 and 0.786 retracement levels**
4. Enter when price reaches this zone AND you have confirmation (OB, FVG, or lower-TF CHoCH)

### OTE + Confluence
- OTE zone containing an Order Block = A+ setup
- OTE zone containing an FVG = A+ setup
- OTE zone at a key liquidity level = A+ setup
- Without confluence, OTE alone is a B setup at best

---

## Power of Three (PO3)

### Definition
Each trading session (and each candle) follows three phases:

### Phase 1: Accumulation
- Price consolidates in a range
- Smart money builds positions quietly
- Appears as low-volume chop

### Phase 2: Manipulation
- Price makes a **false move** (fake breakout) to sweep liquidity
- Retail traders get trapped
- This is the liquidity sweep

### Phase 3: Distribution
- Price reverses sharply in the intended direction
- Smart money distributes to retail traders chasing the move
- This is where the real move happens

### Applying PO3 to Sessions
- **Asia = Accumulation**: Range forms
- **London = Manipulation**: One side of Asia range gets swept
- **New York = Distribution**: The real directional move of the day

---

## Practical Decision Tree

When analyzing current price action, follow this sequence:

```
1. What is the HIGHER TIMEFRAME bias? (Daily/4H trend direction)
   - Bullish: Look for longs only
   - Bearish: Look for shorts only
   - Ranging: Identify the range extremes

2. Where is LIQUIDITY? (Equal highs/lows, swing points)
   - Has it been swept? → Look for reversal setup
   - Not yet swept? → Wait for sweep or trade continuation to the liquidity

3. Is there a CHoCH on your ENTRY TIMEFRAME?
   - Yes → Potential reversal, look for OB/FVG entry
   - No → Trend intact, look for BOS pullback entry

4. Is there an ORDER BLOCK or FVG at current price?
   - Yes → Potential entry zone, confirm with lower TF
   - No → Wait for price to reach a valid zone

5. Is price in the OTE zone (62-79% fib)?
   - Yes → High-probability entry area
   - No → Reduced probability, tighten criteria

6. Are we in a KILL ZONE?
   - Yes → Execute if all criteria met
   - No → Consider waiting or reduce size

7. Does R:R meet minimum threshold (2:1)?
   - Yes → Take the trade
   - No → Pass
```

### Setup Grading
- **A+ Setup**: HTF bias + liquidity sweep + CHoCH + OB/FVG + OTE zone + Kill Zone + R:R >= 3:1
- **A Setup**: HTF bias + OB/FVG + OTE zone + Kill Zone + R:R >= 2:1
- **B Setup**: HTF bias + OB/FVG + R:R >= 2:1 (missing some confluence)
- **C Setup**: Fewer than 3 confluences. Do not trade.

---

## Common Mistakes

1. **Trading against HTF bias**: The #1 mistake. Always align with Daily/4H direction.
2. **Entering without a sweep**: Jumping in before liquidity has been taken.
3. **Using ICT on low-volume sessions**: ICT works best in Kill Zones with displacement.
4. **Ignoring invalidation**: Holding a trade after the OB has been fully violated.
5. **Overcomplicating**: You do not need all concepts on every trade. OB + FVG + HTF bias is enough.
