# Trading Diary Templates Reference
last_verified: 2026-03-22

## Overview

These are raw markdown templates that the skill copies when creating new diary entries. Each template is enclosed in a fenced code block so it can be extracted and used as-is. Replace all placeholder text in `[brackets]` with actual values.

---

## Pre-Market Entry Template

```markdown
# Pre-Market Analysis — [YYYY-MM-DD]

## Overnight Summary
- **Globex Range**: [ONH] - [ONL]
- **Globex Bias**: [Bullish / Bearish / Neutral]
- **Gap**: [Up / Down / None] — [X points from prior RTH close]
- **Key Overnight News**: [Describe any catalysts or events]

## Daily Bias
- **Higher Timeframe Trend (Daily/4H)**: [Bullish / Bearish / Ranging]
- **Bias for Today**: [Long / Short / Neutral]
- **Bias Reasoning**: [Why — e.g., "Daily uptrend, price above 50 EMA, approaching buy-side liquidity"]

## Key Levels
| Level Type         | Price   | Notes                              |
|--------------------|---------|------------------------------------|
| Overnight High     | [price] | [Liquidity target / resistance]    |
| Overnight Low      | [price] | [Liquidity target / support]       |
| Prior Day High     | [price] |                                    |
| Prior Day Low      | [price] |                                    |
| Prior Day POC      | [price] | [Naked? Y/N]                       |
| VAH                | [price] |                                    |
| VAL                | [price] |                                    |
| Key Order Block    | [price zone] | [Timeframe, bull/bear]        |
| Key FVG            | [price zone] | [Timeframe, bull/bear]        |
| Major S/R          | [price] | [Source — e.g., weekly level]      |

## Economic Calendar
| Time (ET) | Event            | Expected Impact | Notes           |
|-----------|------------------|-----------------|-----------------|
| [time]    | [event name]     | [High/Med/Low]  | [prev/forecast] |

## Session Plan
- **Primary Setup**: [e.g., "Long at 15M bullish OB near 5180 if London sweeps ONL"]
- **Secondary Setup**: [e.g., "Short at bearish FVG 5220 if price fails at PDH"]
- **No-Trade Conditions**: [e.g., "No trades before 8:30 AM data, no trades during midday chop"]
- **Max Risk Today**: [$ amount or % of account]
- **Max Trades Today**: [number]

## Mindset Check
- [ ] Slept 7+ hours
- [ ] Feeling calm and focused
- [ ] No external stressors affecting focus
- [ ] Reviewed yesterday's diary
- [ ] Committed to following the plan
```

---

## Trade Log Entry Template

```markdown
## Trade #[N] — [YYYY-MM-DD HH:MM]

### Setup
- **Contract**: [ES / NQ / CL / etc.]
- **Direction**: [Long / Short]
- **Setup Type**: [e.g., Bullish OB + FVG at OTE zone]
- **Timeframe**: [Entry TF — e.g., 5M]
- **HTF Alignment**: [Y/N — describe]
- **Kill Zone**: [London / NY Open / NY PM / None]
- **Setup Grade**: [A+ / A / B / C]

### Execution
| Field              | Value       |
|--------------------|-------------|
| Entry Price        | [price]     |
| Stop Loss          | [price]     |
| Target 1 (1R)     | [price]     |
| Target 2 (2R)     | [price]     |
| Target 3 (3R+)    | [price]     |
| Position Size      | [contracts] |
| Risk ($)           | [$amount]   |
| Risk (% of acct)   | [X%]       |
| R:R Ratio          | [X:1]       |

### Management
- **Partial 1**: [Filled / Not reached] — [price, contracts closed]
- **Stop to BE**: [Y/N — at what time]
- **Partial 2**: [Filled / Not reached] — [price, contracts closed]
- **Final Exit**: [price, reason — target hit / trailed out / stopped out / manual close]

### Result
| Metric             | Value       |
|--------------------|-------------|
| Gross P&L          | [$amount]   |
| Commissions        | [$amount]   |
| Net P&L            | [$amount]   |
| R-Multiple         | [X.XX R]    |
| Hold Time          | [minutes]   |

### Post-Trade Review
- **What went well**: [e.g., "Patient entry, waited for confirmation"]
- **What could improve**: [e.g., "Exited final partial too early"]
- **Rule Adherence Grade**: [A / B / C / D]
- **Screenshot**: [link or file path to chart screenshot]
```

---

## Post-Session Entry Template

```markdown
# Post-Session Review — [YYYY-MM-DD]

## Session Summary
- **Contracts Traded**: [list]
- **Total Trades**: [N]
- **Winners**: [N] | **Losers**: [N] | **Breakeven**: [N]
- **Gross P&L**: [$amount]
- **Net P&L (after commissions)**: [$amount]
- **Win Rate**: [X%]
- **Average R**: [X.XX R]
- **Largest Win**: [$amount] ([X.XX R])
- **Largest Loss**: [$amount] ([X.XX R])

## Plan Adherence
- [ ] Followed pre-market bias? [Y/N — explain if N]
- [ ] Only traded planned setups? [Y/N — explain if N]
- [ ] Respected daily risk limit? [Y/N]
- [ ] Respected max trade count? [Y/N]
- [ ] Executed pre-trade ritual before each trade? [Y/N]
- [ ] Managed partials according to plan? [Y/N]

## Day Type Analysis
- **Market Condition**: [Trending / Ranging / Choppy / Volatile]
- **Day Profile**: [Normal / Normal Variation / Trend / Neutral / Double Distribution]
- **IB Range**: [X points] — [Wide / Normal / Narrow vs average]
- **IB Broken**: [Yes — direction / No]

## What Worked Today
1. [Specific observation]
2. [Specific observation]

## What Did Not Work Today
1. [Specific observation]
2. [Specific observation]

## Lessons / Adjustments
1. [Actionable takeaway for tomorrow]

## Emotional State
- **Pre-session**: [Calm / Anxious / Confident / Tired / etc.]
- **During session**: [Focused / Distracted / Tilted / Patient / etc.]
- **Post-session**: [Satisfied / Frustrated / Neutral / etc.]
- **Tilt detected?**: [Y/N — if Y, what triggered it?]

## Account Status
- **Starting Balance**: [$amount]
- **Ending Balance**: [$amount]
- **Drawdown Used**: [$amount of max drawdown consumed]
- **Drawdown Remaining**: [$amount remaining before violation]
- **Consistency Check**: [Largest day P&L / Total P&L = X% — within limit?]
```

---

## Weekly Review Template

```markdown
# Weekly Review — Week of [YYYY-MM-DD]

## Performance Summary
| Metric              | Value      | Target     | Status       |
|---------------------|-----------|------------|--------------|
| Net P&L             | [$amount] | [target]   | [Met/Missed] |
| Total Trades        | [N]       | --         | --           |
| Win Rate            | [X%]      | > 50%      | [Met/Missed] |
| Average Winner      | [X.XX R]  | > 1.5R     | [Met/Missed] |
| Average Loser       | [X.XX R]  | < 1.0R     | [Met/Missed] |
| Profit Factor       | [X.XX]    | > 1.5      | [Met/Missed] |
| Largest Win         | [$amount] | --         | --           |
| Largest Loss        | [$amount] | --         | --           |
| Max Drawdown (week) | [$amount] | < 2%       | [Met/Missed] |
| A/B Trade %         | [X%]      | > 80%      | [Met/Missed] |

## Daily Breakdown
| Day       | Trades | Win Rate | Net P&L   | Grade |
|-----------|--------|----------|-----------|-------|
| Monday    | [N]    | [X%]     | [$amount] | [A-D] |
| Tuesday   | [N]    | [X%]     | [$amount] | [A-D] |
| Wednesday | [N]    | [X%]     | [$amount] | [A-D] |
| Thursday  | [N]    | [X%]     | [$amount] | [A-D] |
| Friday    | [N]    | [X%]     | [$amount] | [A-D] |

## Best Trade of the Week
- **Description**: [Setup, entry, management, result]
- **What made it great**: [e.g., "Perfect patience, full runner hit 4R"]

## Worst Trade of the Week
- **Description**: [Setup, entry, management, result]
- **What went wrong**: [e.g., "Revenge trade after morning loss, no valid setup"]

## Pattern Recognition
- **Recurring strengths**: [e.g., "Consistently good entries at OB zones"]
- **Recurring weaknesses**: [e.g., "Still exiting runners too early"]
- **Session performance**: [e.g., "NY Open is profitable, PM session is not"]
- **Setup performance**: [e.g., "OB+FVG setups winning 65%, naked FVG setups only 40%"]

## Adjustments for Next Week
1. [Specific, actionable change]
2. [Specific, actionable change]
3. [Specific, actionable change]

## Prop Firm Account Status
| Account    | Starting Bal | Ending Bal | DD Used | DD Remaining | Consistency |
|------------|-------------|-----------|---------|--------------|-------------|
| [Firm/Acct]| [$amount]   | [$amount] | [$amt]  | [$amt]       | [X%]        |
```

---

## Monthly Review Template

```markdown
# Monthly Review — [Month YYYY]

## Performance Summary
| Metric              | Value      | Prior Month | Change   |
|---------------------|-----------|-------------|----------|
| Net P&L             | [$amount] | [$amount]   | [+/- %]  |
| Total Trades        | [N]       | [N]         | [+/- N]  |
| Win Rate            | [X%]      | [X%]        | [+/- %]  |
| Profit Factor       | [X.XX]    | [X.XX]      | [+/- X]  |
| Average R per Trade | [X.XX]    | [X.XX]      | [+/- X]  |
| Max Drawdown        | [$amount] | [$amount]   | [+/- $]  |
| Sharpe Ratio (est)  | [X.XX]    | [X.XX]      | [+/- X]  |
| Trading Days        | [N]       | [N]         |          |
| No-Trade Days       | [N]       | [N]         |          |

## Weekly Breakdown
| Week       | Trades | Win Rate | Net P&L   | PF    |
|------------|--------|----------|-----------|-------|
| Week 1     | [N]    | [X%]     | [$amount] | [X.X] |
| Week 2     | [N]    | [X%]     | [$amount] | [X.X] |
| Week 3     | [N]    | [X%]     | [$amount] | [X.X] |
| Week 4     | [N]    | [X%]     | [$amount] | [X.X] |
| Week 5     | [N]    | [X%]     | [$amount] | [X.X] |

## Setup Analysis
| Setup Type      | Trades | Win Rate | Avg R  | Best for Continued Use? |
|-----------------|--------|----------|--------|--------------------------|
| [OB + FVG]      | [N]    | [X%]    | [X.XX] | [Y/N]                    |
| [ORB]           | [N]    | [X%]    | [X.XX] | [Y/N]                    |
| [Liquidity Sweep]| [N]   | [X%]    | [X.XX] | [Y/N]                    |

## Session Analysis
| Session    | Trades | Win Rate | Net P&L   | Notes              |
|------------|--------|----------|-----------|--------------------|
| London     | [N]    | [X%]     | [$amount] |                    |
| NY Open    | [N]    | [X%]     | [$amount] |                    |
| NY PM      | [N]    | [X%]     | [$amount] |                    |
| Midday     | [N]    | [X%]     | [$amount] |                    |

## Psychology Assessment
- **Discipline score (% A/B trades)**: [X%]
- **Tilt incidents**: [N] — [describe triggers]
- **Revenge trades**: [N] — [describe circumstances]
- **FOMO trades**: [N] — [describe circumstances]
- **Kill switch activations**: [N]

## Key Insights
1. [Major insight from the month's data]
2. [Major insight]
3. [Major insight]

## Goals for Next Month
1. [Specific, measurable goal]
2. [Specific, measurable goal]
3. [Specific, measurable goal]

## Prop Firm Account Status
| Account    | Start of Month | End of Month | Profit Target | Progress | Status    |
|------------|---------------|-------------|---------------|----------|-----------|
| [Firm/Acct]| [$amount]     | [$amount]   | [$target]     | [X%]     | [On track / At risk / Passed / Failed] |
```
