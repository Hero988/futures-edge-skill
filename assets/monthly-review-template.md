# Monthly Review - {MONTH} {YEAR}

**Trading Days:** {TRADING_DAYS_COUNT}
**Instrument(s):** {INSTRUMENTS}
**Account:** {PROP_FIRM} - {ACCOUNT_SIZE}
**Month Grade:** {MONTH_GRADE} (A+ / A / B / C / D / F)

---

## 1. Comprehensive Performance Metrics

### Core Metrics

| Metric | This Month | Prior Month | 3-Month Avg | YTD |
|---|---|---|---|---|
| Net P&L | ${NET_PNL} | ${PRIOR_MONTH_PNL} | ${THREE_MONTH_AVG_PNL} | ${YTD_PNL} |
| Total Trades | {TOTAL_TRADES} | {PRIOR_MONTH_TRADES} | {THREE_MONTH_AVG_TRADES} | {YTD_TRADES} |
| Win Rate | {WIN_RATE}% | {PRIOR_WIN_RATE}% | {THREE_MONTH_AVG_WR}% | {YTD_WR}% |
| Profit Factor | {PROFIT_FACTOR} | {PRIOR_PF} | {THREE_MONTH_AVG_PF} | {YTD_PF} |
| Expectancy (R) | {EXPECTANCY_R}R | {PRIOR_EXPECTANCY}R | {THREE_MONTH_EXPECT}R | {YTD_EXPECT}R |
| Avg Trade (R) | {AVG_TRADE_R}R | {PRIOR_AVG_TRADE}R | {THREE_MONTH_AVG_TRADE}R | {YTD_AVG_TRADE}R |
| Sharpe Ratio | {SHARPE} | {PRIOR_SHARPE} | {THREE_MONTH_SHARPE} | {YTD_SHARPE} |
| Max Drawdown | ${MAX_DD} | ${PRIOR_MAX_DD} | ${THREE_MONTH_MAX_DD} | ${YTD_MAX_DD} |
| Avg Daily P&L | ${AVG_DAILY_PNL} | ${PRIOR_AVG_DAILY} | ${THREE_MONTH_AVG_DAILY} | ${YTD_AVG_DAILY} |
| Std Dev Daily P&L | ${STDEV_DAILY} | ${PRIOR_STDEV} | | |
| Best Day | ${BEST_DAY_PNL} | ${PRIOR_BEST_DAY} | | |
| Worst Day | ${WORST_DAY_PNL} | ${PRIOR_WORST_DAY} | | |
| Max Win Streak | {MAX_WIN_STREAK} | {PRIOR_WIN_STREAK} | | |
| Max Loss Streak | {MAX_LOSS_STREAK} | {PRIOR_LOSS_STREAK} | | |
| Avg Trade Duration | {AVG_DURATION} | {PRIOR_AVG_DURATION} | | |
| Rule Adherence | {RULE_ADHERENCE}% | {PRIOR_RULE_ADHERENCE}% | {THREE_MONTH_RULE}% | {YTD_RULE}% |

### Distribution Metrics

| Metric | Value |
|---|---|
| Winning Days | {WINNING_DAYS} / {TRADING_DAYS_COUNT} ({WINNING_DAYS_PCT}%) |
| Losing Days | {LOSING_DAYS} / {TRADING_DAYS_COUNT} ({LOSING_DAYS_PCT}%) |
| Breakeven Days | {BE_DAYS} / {TRADING_DAYS_COUNT} |
| Avg Winning Day | ${AVG_WINNING_DAY} |
| Avg Losing Day | ${AVG_LOSING_DAY} |
| Win/Loss Day Ratio | {WIN_LOSS_DAY_RATIO} |
| % of P&L from Top 3 Days | {TOP_3_DAYS_PCT}% |
| % of Loss from Bottom 3 Days | {BOTTOM_3_DAYS_PCT}% |

---

## 2. Equity Curve Assessment

### Equity Curve Characteristics
- **Curve Shape:** {CURVE_SHAPE} (Upward / Flat / Downward / V-shaped / Choppy)
- **Smoothness (R-squared):** {R_SQUARED}
- **Recovery Factor:** {RECOVERY_FACTOR}
- **Calmar Ratio:** {CALMAR_RATIO}
- **Underwater Period (max):** {MAX_UNDERWATER_DAYS} days

### Weekly Equity Progression

| Week | Starting Balance | Ending Balance | Weekly P&L | Cumulative P&L |
|---|---|---|---|---|
| Week 1 | ${W1_START} | ${W1_END} | ${W1_PNL} | ${W1_CUM} |
| Week 2 | ${W2_START} | ${W2_END} | ${W2_PNL} | ${W2_CUM} |
| Week 3 | ${W3_START} | ${W3_END} | ${W3_PNL} | ${W3_CUM} |
| Week 4 | ${W4_START} | ${W4_END} | ${W4_PNL} | ${W4_CUM} |
| Week 5 | ${W5_START} | ${W5_END} | ${W5_PNL} | ${W5_CUM} |

### Drawdown Log

| Start Date | End Date | Depth ($) | Depth (%) | Duration (days) | Recovery (days) | Cause |
|---|---|---|---|---|---|---|
| {DD_START_1} | {DD_END_1} | ${DD_DEPTH_1} | {DD_PCT_1}% | {DD_DURATION_1} | {DD_RECOVERY_1} | {DD_CAUSE_1} |
| {DD_START_2} | {DD_END_2} | ${DD_DEPTH_2} | {DD_PCT_2}% | {DD_DURATION_2} | {DD_RECOVERY_2} | {DD_CAUSE_2} |
| {DD_START_3} | {DD_END_3} | ${DD_DEPTH_3} | {DD_PCT_3}% | {DD_DURATION_3} | {DD_RECOVERY_3} | {DD_CAUSE_3} |

---

## 3. Setup-by-Setup Breakdown

| Setup | Trades | Win Rate | Avg Win (R) | Avg Loss (R) | Expectancy (R) | Total R | Net P&L | PF | Grade |
|---|---|---|---|---|---|---|---|---|---|
| {SETUP_1} | {S1_TRADES} | {S1_WR}% | {S1_AVG_WIN}R | {S1_AVG_LOSS}R | {S1_EXPECT}R | {S1_TOTAL_R}R | ${S1_PNL} | {S1_PF} | {S1_GRADE} |
| {SETUP_2} | {S2_TRADES} | {S2_WR}% | {S2_AVG_WIN}R | {S2_AVG_LOSS}R | {S2_EXPECT}R | {S2_TOTAL_R}R | ${S2_PNL} | {S2_PF} | {S2_GRADE} |
| {SETUP_3} | {S3_TRADES} | {S3_WR}% | {S3_AVG_WIN}R | {S3_AVG_LOSS}R | {S3_EXPECT}R | {S3_TOTAL_R}R | ${S3_PNL} | {S3_PF} | {S3_GRADE} |
| {SETUP_4} | {S4_TRADES} | {S4_WR}% | {S4_AVG_WIN}R | {S4_AVG_LOSS}R | {S4_EXPECT}R | {S4_TOTAL_R}R | ${S4_PNL} | {S4_PF} | {S4_GRADE} |
| {SETUP_5} | {S5_TRADES} | {S5_WR}% | {S5_AVG_WIN}R | {S5_AVG_LOSS}R | {S5_EXPECT}R | {S5_TOTAL_R}R | ${S5_PNL} | {S5_PF} | {S5_GRADE} |

### Setup Decisions
- **Keep (performing well):** {KEEP_SETUPS}
- **Optimize (underperforming):** {OPTIMIZE_SETUPS}
- **Remove (negative expectancy):** {REMOVE_SETUPS}
- **Add (new setups to test):** {ADD_SETUPS}

---

## 4. Strategy Health Status

### Strategy Vitals

| Strategy Component | Status | Health | Action Required |
|---|---|---|---|
| Edge Integrity | {EDGE_STATUS} | {EDGE_HEALTH} (Healthy / Degrading / Failed) | {EDGE_ACTION} |
| Risk Management | {RISK_STATUS} | {RISK_HEALTH} | {RISK_ACTION} |
| Trade Management | {MGMT_STATUS} | {MGMT_HEALTH} | {MGMT_ACTION} |
| Entry Timing | {ENTRY_STATUS} | {ENTRY_HEALTH} | {ENTRY_ACTION} |
| Exit Strategy | {EXIT_STATUS} | {EXIT_HEALTH} | {EXIT_ACTION} |
| Position Sizing | {SIZING_STATUS} | {SIZING_HEALTH} | {SIZING_ACTION} |
| Emotional Discipline | {EMOTIONAL_STATUS} | {EMOTIONAL_HEALTH} | {EMOTIONAL_ACTION} |

### Market Regime Assessment
- **Current Regime:** {MARKET_REGIME} (Trending / Mean-Reverting / Volatile / Low-Vol / Transitioning)
- **Strategy-Regime Fit:** {REGIME_FIT} (Strong / Moderate / Weak)
- **Adaptation Needed:** {ADAPTATION_NEEDED} (Yes / No)
- **Notes:** {REGIME_NOTES}

---

## 5. Prop Firm Evaluation Progress

### Account Status

| Metric | Start of Month | End of Month | Change |
|---|---|---|---|
| Account Balance | ${BALANCE_START} | ${BALANCE_END} | ${BALANCE_CHANGE} |
| Drawdown Floor | ${DD_FLOOR_START} | ${DD_FLOOR_END} | ${DD_FLOOR_CHANGE} |
| Drawdown Remaining | ${DD_REMAINING_START} | ${DD_REMAINING_END} | ${DD_REMAINING_CHANGE} |
| Profit Target Remaining | ${TARGET_REMAINING_START} | ${TARGET_REMAINING_END} | ${TARGET_REMAINING_CHANGE} |
| Trading Days | {DAYS_START} | {DAYS_END} | +{DAYS_ADDED} |

### Evaluation Trajectory
- **Target Completion:** {TARGET_COMPLETION_PCT}%
- **Projected Days to Complete:** {PROJECTED_DAYS}
- **Consistency Rule Status:** {CONSISTENCY_STATUS}
- **Best Single Day:** ${BEST_SINGLE_DAY} ({BEST_DAY_PCT}% of total)
- **On Track:** {ON_TRACK} (Yes / No / At Risk)

### Compliance Summary

| Rule | Violations This Month | Total Violations | Trend |
|---|---|---|---|
| Daily Loss Limit | {DLL_VIOLATIONS} | {DLL_TOTAL} | {DLL_TREND} |
| Position Limits | {POS_VIOLATIONS} | {POS_TOTAL} | {POS_TREND} |
| Close By Time | {CLOSE_VIOLATIONS} | {CLOSE_TOTAL} | {CLOSE_TREND} |
| News Blackout | {NEWS_VIOLATIONS} | {NEWS_TOTAL} | {NEWS_TREND} |
| Consistency Rule | {CONSIST_VIOLATIONS} | {CONSIST_TOTAL} | {CONSIST_TREND} |
| Overnight Positions | {OVERNIGHT_VIOLATIONS} | {OVERNIGHT_TOTAL} | {OVERNIGHT_TREND} |

---

## 6. Rule Evolution Summary

### Rules Added This Month
1. {NEW_RULE_1}
2. {NEW_RULE_2}

### Rules Modified This Month
1. {MODIFIED_RULE_1} -- Reason: {MODIFY_REASON_1}
2. {MODIFIED_RULE_2} -- Reason: {MODIFY_REASON_2}

### Rules Removed This Month
1. {REMOVED_RULE_1} -- Reason: {REMOVE_REASON_1}

### Rule Effectiveness Assessment
| Rule | Adherence Rate | P&L Impact When Followed | P&L Impact When Broken | Verdict |
|---|---|---|---|---|
| {RULE_NAME_1} | {RULE_ADHERENCE_1}% | ${RULE_FOLLOWED_PNL_1} | ${RULE_BROKEN_PNL_1} | {RULE_VERDICT_1} |
| {RULE_NAME_2} | {RULE_ADHERENCE_2}% | ${RULE_FOLLOWED_PNL_2} | ${RULE_BROKEN_PNL_2} | {RULE_VERDICT_2} |
| {RULE_NAME_3} | {RULE_ADHERENCE_3}% | ${RULE_FOLLOWED_PNL_3} | ${RULE_BROKEN_PNL_3} | {RULE_VERDICT_3} |

---

## 7. Verification Status

### Data Integrity
- [ ] All trades logged and reconciled with broker statements
- [ ] P&L matches broker account statement
- [ ] All commissions and fees accounted for
- [ ] Drawdown calculations verified
- [ ] Consistency rule calculations verified

### Process Verification
- [ ] Pre-market checklist completed every trading day
- [ ] Post-session review completed every trading day
- [ ] Weekly reviews completed for all weeks
- [ ] Trade screenshots archived
- [ ] Diary entries made for significant events

### External Verification
- **Broker Statement Match:** {BROKER_MATCH} (Yes / No / Partial)
- **Discrepancy Amount:** ${DISCREPANCY}
- **Discrepancy Cause:** {DISCREPANCY_CAUSE}

---

## 8. Goals Assessment

### Last Month's Goals

| Goal | Target | Actual | Met |
|---|---|---|---|
| {LAST_GOAL_1} | {LAST_TARGET_1} | {LAST_ACTUAL_1} | {LAST_MET_1} |
| {LAST_GOAL_2} | {LAST_TARGET_2} | {LAST_ACTUAL_2} | {LAST_MET_2} |
| {LAST_GOAL_3} | {LAST_TARGET_3} | {LAST_ACTUAL_3} | {LAST_MET_3} |
| {LAST_GOAL_4} | {LAST_TARGET_4} | {LAST_ACTUAL_4} | {LAST_MET_4} |

### Goals for Next Month

#### Performance Goals
1. {NEXT_PERF_GOAL_1}
2. {NEXT_PERF_GOAL_2}

#### Process Goals
1. {NEXT_PROCESS_GOAL_1}
2. {NEXT_PROCESS_GOAL_2}
3. {NEXT_PROCESS_GOAL_3}

#### Development Goals
1. {NEXT_DEV_GOAL_1}
2. {NEXT_DEV_GOAL_2}

#### Mental / Emotional Goals
1. {NEXT_MENTAL_GOAL_1}
2. {NEXT_MENTAL_GOAL_2}

---

## 9. Monthly Reflection

### What defined this month?
> {MONTH_DEFINITION}

### What is my biggest edge right now?
> {BIGGEST_EDGE}

### What is my biggest weakness right now?
> {BIGGEST_WEAKNESS}

### Am I on the right path?
> {RIGHT_PATH}

### One thing to carry forward:
> {CARRY_FORWARD}

---

*Reviewed: {REVIEW_TIMESTAMP}*
*Monthly review version: 1.0*
