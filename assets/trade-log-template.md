# Trade Log Entry

## Trade #{TRADE_NUMBER}

**Date:** {DATE}
**Day of Week:** {DAY_OF_WEEK}
**Session:** {SESSION} (RTH / ETH)

---

## Setup

| Field | Value |
|---|---|
| Instrument | {INSTRUMENT} |
| Direction | {DIRECTION} (Long / Short) |
| Setup Type | {SETUP_TYPE} |
| Timeframe | {TIMEFRAME} |
| Confluence Score | {CONFLUENCE_SCORE} / 5 |
| Grade | {SETUP_GRADE} (A+ / A / B / C) |

### Confluence Factors
- [ ] {CONFLUENCE_1}
- [ ] {CONFLUENCE_2}
- [ ] {CONFLUENCE_3}
- [ ] {CONFLUENCE_4}
- [ ] {CONFLUENCE_5}

### Setup Narrative
{SETUP_NARRATIVE}

---

## Levels

| Level | Planned | Actual |
|---|---|---|
| Entry | {PLANNED_ENTRY} | {ACTUAL_ENTRY} |
| Stop Loss | {PLANNED_STOP} | {ACTUAL_STOP} |
| Target 1 | {PLANNED_T1} | {ACTUAL_T1} |
| Target 2 | {PLANNED_T2} | {ACTUAL_T2} |
| Runner Target | {PLANNED_RUNNER} | {ACTUAL_RUNNER} |

| Metric | Value |
|---|---|
| Initial Risk (pts) | {INITIAL_RISK_PTS} |
| Initial Risk ($) | ${INITIAL_RISK_DOLLARS} |
| T1 R:R | {T1_RR} |
| T2 R:R | {T2_RR} |
| Runner R:R | {RUNNER_RR} |

---

## Execution

| Field | Value |
|---|---|
| Entry Time | {ENTRY_TIME} |
| Exit Time | {EXIT_TIME} |
| Duration | {TRADE_DURATION} |
| Contracts | {CONTRACTS} |
| Entry Method | {ENTRY_METHOD} (Limit / Market / Stop) |
| Slippage (ticks) | {SLIPPAGE_TICKS} |
| Slippage ($) | ${SLIPPAGE_DOLLARS} |
| Commission | ${COMMISSION} |

### Partial Exits

| Exit # | Time | Contracts | Price | P&L | Reason |
|---|---|---|---|---|---|
| 1 | {PARTIAL_TIME_1} | {PARTIAL_CONTRACTS_1} | {PARTIAL_PRICE_1} | ${PARTIAL_PNL_1} | {PARTIAL_REASON_1} |
| 2 | {PARTIAL_TIME_2} | {PARTIAL_CONTRACTS_2} | {PARTIAL_PRICE_2} | ${PARTIAL_PNL_2} | {PARTIAL_REASON_2} |
| 3 | {PARTIAL_TIME_3} | {PARTIAL_CONTRACTS_3} | {PARTIAL_PRICE_3} | ${PARTIAL_PNL_3} | {PARTIAL_REASON_3} |

---

## Result

| Metric | Value |
|---|---|
| Gross P&L | ${GROSS_PNL} |
| Net P&L (after commissions) | ${NET_PNL} |
| P&L in R | {PNL_IN_R}R |
| Outcome | {OUTCOME} (Win / Loss / Breakeven / Scratch) |
| MAE (Max Adverse Excursion) | {MAE_PTS} pts / ${MAE_DOLLARS} |
| MFE (Max Favorable Excursion) | {MFE_PTS} pts / ${MFE_DOLLARS} |
| Capture Ratio (P&L / MFE) | {CAPTURE_RATIO}% |

---

## Trade Analysis

### Execution Quality

| Category | Score (1-5) | Notes |
|---|---|---|
| Entry Quality | {ENTRY_QUALITY} | {ENTRY_QUALITY_NOTES} |
| Exit Quality | {EXIT_QUALITY} | {EXIT_QUALITY_NOTES} |
| Position Sizing | {SIZING_QUALITY} | {SIZING_QUALITY_NOTES} |
| Trade Management | {MANAGEMENT_QUALITY} | {MANAGEMENT_QUALITY_NOTES} |
| Followed Plan | {FOLLOWED_PLAN} | {PLAN_ADHERENCE_NOTES} |

### Emotional State

| Timing | State | Notes |
|---|---|---|
| Pre-Trade | {EMOTION_PRE} (Calm / Anxious / FOMO / Revenge / Confident / Overconfident) | {EMOTION_PRE_NOTES} |
| During Trade | {EMOTION_DURING} (Calm / Anxious / Hopeful / Fearful / Greedy / Disciplined) | {EMOTION_DURING_NOTES} |
| Post-Trade | {EMOTION_POST} (Satisfied / Frustrated / Relieved / Regretful / Neutral) | {EMOTION_POST_NOTES} |

### What Went Well
- {WENT_WELL_1}
- {WENT_WELL_2}

### What Could Improve
- {IMPROVE_1}
- {IMPROVE_2}

### Lesson
> {TRADE_LESSON}

---

## Prop Firm Compliance Check

| Check | Value | Status |
|---|---|---|
| Daily P&L After This Trade | ${DAILY_PNL_AFTER} | {DAILY_PNL_STATUS} |
| Drawdown Remaining | ${DRAWDOWN_REMAINING} | {DRAWDOWN_STATUS} |
| Trades Today | {TRADES_TODAY} / {MAX_TRADES_TODAY} | {TRADES_STATUS} |
| Within Position Limits | {POSITION_LIMIT_CHECK} | {POSITION_STATUS} |
| Consistency Rule | {CONSISTENCY_CHECK} | {CONSISTENCY_STATUS} |
| News Blackout Respected | {NEWS_BLACKOUT_CHECK} | {NEWS_STATUS} |
| Close By Time Respected | {CLOSE_BY_CHECK} | {CLOSE_BY_STATUS} |
| **Overall Compliance** | | **{OVERALL_COMPLIANCE}** |

---

## Screenshots

- Entry: {SCREENSHOT_ENTRY_PATH}
- Exit: {SCREENSHOT_EXIT_PATH}
- Context: {SCREENSHOT_CONTEXT_PATH}

---

*Logged: {LOGGED_TIMESTAMP}*
*Trade log version: 1.0*
