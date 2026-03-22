# Session Playbook Reference
last_verified: 2026-03-22

## Overview

Futures markets trade nearly 24 hours, but not all hours are equal. Volume, volatility, and opportunity concentrate in specific windows. This playbook defines each session, its characteristics, and optimal strategies.

All times are Eastern Time (ET).

---

## Globex / Overnight Session (6:00 PM - 9:30 AM ET)

### Characteristics
- Low volume relative to RTH (typically 20-40% of RTH volume)
- Price discovery driven by international events, earnings, and economic data
- Defines the overnight high and low, which are key levels for RTH

### Key Levels to Mark
- **Overnight High (ONH)**: Resistance / liquidity target at RTH open
- **Overnight Low (ONL)**: Support / liquidity target at RTH open
- **Globex VWAP**: Separate from RTH VWAP, acts as bias filter for overnight traders

### Gap Analysis
- **True gap**: RTH open outside prior RTH close range. Gaps > 0.5% have 70%+ fill rate within the session.
- **Gap and go**: Open strongly directional, do not fade. Wait for first pullback to enter with trend.
- **Gap and fill**: Open, initial move to fill gap, then resume. Trade the fill if it aligns with bias.
- **Gap rules**: If gap > 1%, wait 15 minutes before trading. Let the market establish direction.

---

## London Session / ICT Kill Zone (2:00 AM - 5:00 AM ET)

### Characteristics
- High impact for FX futures: 6E (Euro), 6B (British Pound), 6J (Yen)
- Often sets the high or low of the entire day
- Institutional activity begins in earnest
- Liquidity sweep of Asia range is the primary setup

### Primary Setup: Asia Range Sweep
1. Mark Asia session high and low (7 PM - 2 AM ET)
2. London opens and sweeps one side of the Asia range (usually within the first 30-60 min)
3. After the sweep, look for CHoCH on 5M or 15M
4. Enter on the reversal targeting the opposite side of the Asia range (minimum target)
5. Extended target: sweep of the other side of the Asia range

### London Session Rules
- If London does not sweep Asia range by 4 AM ET, the setup is less reliable
- London high or low formed before 5 AM ET is a key level for NY session
- High-impact UK/EU economic data (CPI, PMI, ECB) creates extra volatility

---

## New York Open / ICT Kill Zone (8:30 AM - 11:00 AM ET)

### Characteristics
- Highest volume period for index futures (ES, NQ, YM, RTY)
- Economic data releases at 8:30 AM (NFP, CPI, GDP, Jobless Claims)
- 9:30 AM RTH open brings additional volume surge
- Most displacement and ICT setups occur here

### Primary Setups

#### Opening Range Breakout (ORB)
1. Define the first 15-minute or 30-minute range after RTH open (9:30 AM)
2. Mark the high and low of this range
3. Enter on a break above/below with volume confirmation
4. Target: 1x the opening range height
5. Stop: Opposite side of the opening range
6. Filter: Only take ORB in the direction of VWAP bias (above VWAP = long breakout only)

#### London High/Low Sweep
1. Mark London session high and low
2. NY session sweeps one of these levels (common within 9:30-10:30 AM)
3. After sweep + CHoCH on 5M, enter reversal
4. Target: Opposite London extreme or developing VPOC

#### 8:30 AM Data Play
1. Major data release at 8:30 AM creates a spike
2. Do NOT trade the initial spike (too fast, too random)
3. Wait 5-15 minutes for the dust to settle
4. Identify which side of VWAP price settles on
5. Enter on the first clean pullback to VWAP or key EMA

### NY Open Rules
- First 5 minutes of RTH (9:30-9:35) are chaotic. Observe, do not trade.
- Best entries: 9:45-10:30 AM after initial volatility subsides
- If no setup by 11:00 AM, stop looking. Move on to midday or PM session.

---

## New York Midday (11:00 AM - 1:30 PM ET)

### Characteristics
- Volume drops significantly
- Price typically enters a range/consolidation
- Choppy, mean-reverting price action
- This is where most overtrading losses occur

### Rules
- **Default action: Do NOT trade this window** unless there is a clear trend day in progress
- If the day is trending (IB extended > 2x average), midday is a continuation zone. Trail stops, do not take new positions against the trend.
- If the day is ranging, midday will chop between morning high/low. Sit out.
- Use this time for: analysis, journaling, marking PM session levels, reviewing the morning

### Exception: Midday Reversal
- If price has trended all morning and reaches a major HTF level (daily OB, weekly FVG), a midday reversal can occur
- Confirmation: CHoCH on 15M + delta divergence + RSI divergence
- These are rare but powerful. Only take with strong confluence.

---

## New York PM / ICT Kill Zone (1:30 PM - 4:00 PM ET)

### Characteristics
- Volume picks back up
- Second major opportunity window of the day
- Often: PM session either extends the AM move OR reverses it
- MOC (Market on Close) imbalances published after 3:30 PM create late volatility

### Primary Setups

#### PM Reversal
1. If AM session was strongly one-directional, PM session may reverse
2. Look for: liquidity sweep of the AM extreme, CHoCH on 15M, entry at OB/FVG
3. Target: VWAP or AM session midpoint

#### PM Continuation
1. If AM session established a trend, PM session extends it
2. Enter on pullback to VWAP or 21 EMA
3. Target: Next major level (prior day high/low, weekly level)

#### MOC Imbalance Play (3:30 PM - 3:50 PM)
1. NYSE MOC imbalances published after 3:30 PM
2. Large buy imbalance = expect late rally. Large sell = expect late selloff.
3. Enter in imbalance direction on first pullback after 3:30 PM
4. Exit by 3:50 PM (before close volatility becomes unpredictable)

### PM Session Rules
- If no clear setup by 2:30 PM, the PM session may be dead. Do not force it.
- Many prop firms require closing positions by 3:10-3:59 PM. Plan exit timing accordingly.
- The last 10 minutes (3:50-4:00 PM) are extremely volatile. Exit before or use tight stops.

---

## Asia Session (7:00 PM - 2:00 AM ET)

### Characteristics
- Lowest volume of any session for index futures
- Accumulation/consolidation phase
- Defines the Asia range that London will target
- Primarily useful for marking levels, not for active trading

### Rules
- Generally do NOT actively trade index futures during Asia session
- Exception: Major overnight catalysts (FOMC statement reaction, geopolitical events, earnings from mega-caps)
- Use Asia session to: mark ONH/ONL, identify Asia range for London sweep setup, review bias

---

## Best Trading Times by Contract

| Contract | Peak Volume Window     | Notes                                    |
|----------|------------------------|------------------------------------------|
| ES/MES   | 9:30 - 11:30 AM ET    | Also good 1:30 - 3:30 PM                |
| NQ/MNQ   | 9:30 - 11:00 AM ET    | Most volatile of index futures           |
| YM/MYM   | 9:30 - 11:00 AM ET    | Follows ES closely                       |
| RTY/M2K  | 9:30 - 11:00 AM ET    | Widest spreads of index futures          |
| CL/MCL   | 9:00 - 10:30 AM ET    | EIA inventory Wed 10:30 AM = high vol    |
| GC/MGC   | 8:30 - 10:00 AM ET    | Reacts to USD data, London overlap       |

---

## When to NOT Trade

### Mandatory No-Trade Windows
- **First 5 minutes of RTH (9:30-9:35 AM)**: Too chaotic, wide spreads, stop hunts
- **Last 5 minutes of RTH (3:55-4:00 PM)**: Erratic MOC flows, unpredictable
- **FOMC day before announcement (2:00 PM ET)**: Dead volume, then explosion. Wait until 2:30 PM for dust to settle.
- **NFP release day**: Wait until 9:00 AM for dust to settle after 8:30 AM release

### Conditional No-Trade Days
- **Low-volume holidays**: Half days (day before Thanksgiving, Christmas Eve, etc.). Thin markets = random moves.
- **Friday afternoon after 2:00 PM**: Weekend risk-off, low volume, position squaring
- **3+ consecutive red days in your diary**: You are likely tilted. See psychology reference. Reduce or sit out.
- **Major geopolitical events**: War escalation, sudden policy changes. Sit out initial reaction.

### Prop Firm Calendar Awareness
- Know your firm's restricted days (some close early before holidays)
- Know your firm's news blackout rules (some auto-liquidate within 2 min of major data)
- Check the economic calendar every morning before placing any trade
