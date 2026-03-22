# Backtest Report

## Strategy Overview

| Field | Value |
|---|---|
| Strategy Name | {STRATEGY_NAME} |
| Version | {STRATEGY_VERSION} |
| Date | {REPORT_DATE} |
| Instrument | {INSTRUMENT} |
| Timeframe | {TIMEFRAME} |
| Direction | {DIRECTION} (Long Only / Short Only / Both) |
| Data Source | {DATA_SOURCE} |
| Commission/Slippage Model | {COMMISSION_MODEL} |

### Strategy Description
{STRATEGY_DESCRIPTION}

### Entry Rules
1. {ENTRY_RULE_1}
2. {ENTRY_RULE_2}
3. {ENTRY_RULE_3}
4. {ENTRY_RULE_4}

### Exit Rules
1. {EXIT_RULE_1}
2. {EXIT_RULE_2}
3. {EXIT_RULE_3}

### Filters
1. {FILTER_1}
2. {FILTER_2}
3. {FILTER_3}

---

## 1. Summary Metrics

### In-Sample (IS) vs Out-of-Sample (OOS)

| Metric | In-Sample | Out-of-Sample | Degradation |
|---|---|---|---|
| Period | {IS_PERIOD} | {OOS_PERIOD} | N/A |
| Total Trades | {IS_TRADES} | {OOS_TRADES} | {TRADES_DEGRADE}% |
| Win Rate | {IS_WIN_RATE}% | {OOS_WIN_RATE}% | {WR_DEGRADE}% |
| Profit Factor | {IS_PF} | {OOS_PF} | {PF_DEGRADE}% |
| Sharpe Ratio | {IS_SHARPE} | {OOS_SHARPE} | {SHARPE_DEGRADE}% |
| Sortino Ratio | {IS_SORTINO} | {OOS_SORTINO} | {SORTINO_DEGRADE}% |
| Max Drawdown ($) | ${IS_MAX_DD} | ${OOS_MAX_DD} | {DD_DEGRADE}% |
| Max Drawdown (%) | {IS_MAX_DD_PCT}% | {OOS_MAX_DD_PCT}% | |
| Expectancy (R) | {IS_EXPECTANCY}R | {OOS_EXPECTANCY}R | {EXPECT_DEGRADE}% |
| Expectancy ($) | ${IS_EXPECTANCY_DOLLAR} | ${OOS_EXPECTANCY_DOLLAR} | |
| Net P&L | ${IS_NET_PNL} | ${OOS_NET_PNL} | {PNL_DEGRADE}% |
| Avg Trade ($) | ${IS_AVG_TRADE} | ${OOS_AVG_TRADE} | {AVG_TRADE_DEGRADE}% |
| Avg Winner ($) | ${IS_AVG_WIN} | ${OOS_AVG_WIN} | |
| Avg Loser ($) | ${IS_AVG_LOSS} | ${OOS_AVG_LOSS} | |
| Avg Winner (R) | {IS_AVG_WIN_R}R | {OOS_AVG_WIN_R}R | |
| Avg Loser (R) | {IS_AVG_LOSS_R}R | {OOS_AVG_LOSS_R}R | |
| Largest Win | ${IS_LARGEST_WIN} | ${OOS_LARGEST_WIN} | |
| Largest Loss | ${IS_LARGEST_LOSS} | ${OOS_LARGEST_LOSS} | |
| Max Consecutive Wins | {IS_MAX_WINS} | {OOS_MAX_WINS} | |
| Max Consecutive Losses | {IS_MAX_LOSSES} | {OOS_MAX_LOSSES} | |
| Avg Trade Duration | {IS_AVG_DURATION} | {OOS_AVG_DURATION} | |
| Recovery Factor | {IS_RECOVERY} | {OOS_RECOVERY} | |
| Calmar Ratio | {IS_CALMAR} | {OOS_CALMAR} | |
| Ulcer Index | {IS_ULCER} | {OOS_ULCER} | |

### OOS Degradation Threshold
- **Acceptable:** < 20% degradation across key metrics
- **Marginal:** 20-40% degradation
- **Fail:** > 40% degradation
- **Overall OOS Degradation:** {OVERALL_DEGRADE}% -- **{DEGRADE_VERDICT}**

---

## 2. Walk-Forward Analysis

### Configuration
- **Total Period:** {WF_TOTAL_PERIOD}
- **IS Window:** {WF_IS_WINDOW}
- **OOS Window:** {WF_OOS_WINDOW}
- **Anchored:** {WF_ANCHORED} (Yes / No)
- **Number of Folds:** {WF_FOLDS}

### Walk-Forward Results

| Fold | IS Period | OOS Period | IS PF | OOS PF | IS WR | OOS WR | IS Sharpe | OOS Sharpe | OOS P&L |
|---|---|---|---|---|---|---|---|---|---|
| 1 | {WF_IS_1} | {WF_OOS_1} | {WF_IS_PF_1} | {WF_OOS_PF_1} | {WF_IS_WR_1}% | {WF_OOS_WR_1}% | {WF_IS_SHARPE_1} | {WF_OOS_SHARPE_1} | ${WF_OOS_PNL_1} |
| 2 | {WF_IS_2} | {WF_OOS_2} | {WF_IS_PF_2} | {WF_OOS_PF_2} | {WF_IS_WR_2}% | {WF_OOS_WR_2}% | {WF_IS_SHARPE_2} | {WF_OOS_SHARPE_2} | ${WF_OOS_PNL_2} |
| 3 | {WF_IS_3} | {WF_OOS_3} | {WF_IS_PF_3} | {WF_OOS_PF_3} | {WF_IS_WR_3}% | {WF_OOS_WR_3}% | {WF_IS_SHARPE_3} | {WF_OOS_SHARPE_3} | ${WF_OOS_PNL_3} |
| 4 | {WF_IS_4} | {WF_OOS_4} | {WF_IS_PF_4} | {WF_OOS_PF_4} | {WF_IS_WR_4}% | {WF_OOS_WR_4}% | {WF_IS_SHARPE_4} | {WF_OOS_SHARPE_4} | ${WF_OOS_PNL_4} |
| 5 | {WF_IS_5} | {WF_OOS_5} | {WF_IS_PF_5} | {WF_OOS_PF_5} | {WF_IS_WR_5}% | {WF_OOS_WR_5}% | {WF_IS_SHARPE_5} | {WF_OOS_SHARPE_5} | ${WF_OOS_PNL_5} |
| 6 | {WF_IS_6} | {WF_OOS_6} | {WF_IS_PF_6} | {WF_OOS_PF_6} | {WF_IS_WR_6}% | {WF_OOS_WR_6}% | {WF_IS_SHARPE_6} | {WF_OOS_SHARPE_6} | ${WF_OOS_PNL_6} |

### Walk-Forward Summary
- **OOS Profitable Folds:** {WF_PROFITABLE_FOLDS} / {WF_FOLDS} ({WF_PROFITABLE_PCT}%)
- **Walk-Forward Efficiency:** {WF_EFFICIENCY}% (OOS avg performance / IS avg performance)
- **Parameter Stability:** {PARAM_STABILITY} (Stable / Moderate / Unstable)
- **Walk-Forward Verdict:** **{WF_VERDICT}** (PASS / MARGINAL / FAIL)

### Walk-Forward Pass Criteria
- At least 70% of OOS folds profitable
- Walk-forward efficiency > 50%
- Parameters remain within stable ranges across folds

---

## 3. Monte Carlo Simulation

### Configuration
- **Simulations:** {MC_SIMULATIONS}
- **Method:** {MC_METHOD} (Trade Resampling / Return Shuffling / Both)
- **Confidence Level:** {MC_CONFIDENCE}%

### Monte Carlo Results

| Metric | Median | 5th Percentile | 25th Percentile | 75th Percentile | 95th Percentile |
|---|---|---|---|---|---|
| Net P&L | ${MC_PNL_MEDIAN} | ${MC_PNL_5} | ${MC_PNL_25} | ${MC_PNL_75} | ${MC_PNL_95} |
| Max Drawdown ($) | ${MC_DD_MEDIAN} | ${MC_DD_5} | ${MC_DD_25} | ${MC_DD_75} | ${MC_DD_95} |
| Max Drawdown (%) | {MC_DD_PCT_MEDIAN}% | {MC_DD_PCT_5}% | {MC_DD_PCT_25}% | {MC_DD_PCT_75}% | {MC_DD_PCT_95}% |
| Win Rate | {MC_WR_MEDIAN}% | {MC_WR_5}% | {MC_WR_25}% | {MC_WR_75}% | {MC_WR_95}% |
| Profit Factor | {MC_PF_MEDIAN} | {MC_PF_5} | {MC_PF_25} | {MC_PF_75} | {MC_PF_95} |
| Sharpe Ratio | {MC_SHARPE_MEDIAN} | {MC_SHARPE_5} | {MC_SHARPE_25} | {MC_SHARPE_75} | {MC_SHARPE_95} |
| Max Consec. Losses | {MC_CONSEC_LOSS_MEDIAN} | {MC_CONSEC_LOSS_5} | {MC_CONSEC_LOSS_25} | {MC_CONSEC_LOSS_75} | {MC_CONSEC_LOSS_95} |
| Longest DD (days) | {MC_DD_DAYS_MEDIAN} | {MC_DD_DAYS_5} | {MC_DD_DAYS_25} | {MC_DD_DAYS_75} | {MC_DD_DAYS_95} |

### Risk of Ruin Analysis
- **Probability of 10% Drawdown:** {PROB_10_DD}%
- **Probability of 20% Drawdown:** {PROB_20_DD}%
- **Probability of 30% Drawdown:** {PROB_30_DD}%
- **Probability of Ruin (50% DD):** {PROB_RUIN}%
- **Risk of Ruin Verdict:** **{ROR_VERDICT}** (Safe / Acceptable / Elevated / Dangerous)

---

## 4. Prop Firm Simulation

### Configuration
- **Prop Firm:** {SIM_PROP_FIRM}
- **Account Size:** {SIM_ACCOUNT_SIZE}
- **Drawdown Type:** {SIM_DD_TYPE}
- **Max Drawdown:** ${SIM_MAX_DD}
- **Daily Loss Limit:** ${SIM_DAILY_LIMIT}
- **Profit Target:** ${SIM_PROFIT_TARGET}
- **Consistency Rule:** {SIM_CONSISTENCY}
- **Monte Carlo Runs:** {SIM_MC_RUNS}

### Simulation Results

| Metric | Median | 5th Percentile | 95th Percentile |
|---|---|---|---|
| Days to Pass | {SIM_DAYS_MEDIAN} | {SIM_DAYS_5} | {SIM_DAYS_95} |
| Pass Rate | {SIM_PASS_RATE}% | | |
| Fail by Drawdown | {SIM_FAIL_DD}% | | |
| Fail by Daily Limit | {SIM_FAIL_DAILY}% | | |
| Fail by Consistency | {SIM_FAIL_CONSIST}% | | |
| Ending Balance (if passed) | ${SIM_END_BAL_MEDIAN} | ${SIM_END_BAL_5} | ${SIM_END_BAL_95} |
| Max DD During Pass | ${SIM_MAX_DD_PASS_MEDIAN} | ${SIM_MAX_DD_PASS_5} | ${SIM_MAX_DD_PASS_95} |

### Expected Cost Analysis
- **Expected Attempts to Pass:** {EXPECTED_ATTEMPTS}
- **Cost Per Attempt:** ${COST_PER_ATTEMPT}
- **Expected Total Cost:** ${EXPECTED_TOTAL_COST}
- **Expected Time to Pass:** {EXPECTED_TIME_WEEKS} weeks
- **ROI if Funded (first 3 months):** {EXPECTED_ROI}%

### Prop Firm Simulation Verdict: **{SIM_VERDICT}** (VIABLE / MARGINAL / NOT VIABLE)

---

## 5. Parameter Sensitivity

### Key Parameters Tested

| Parameter | Optimal | -20% | -10% | +10% | +20% | Sensitivity |
|---|---|---|---|---|---|---|
| {PARAM_1_NAME} | {P1_OPTIMAL} | {P1_MINUS_20} | {P1_MINUS_10} | {P1_PLUS_10} | {P1_PLUS_20} | {P1_SENSITIVITY} |
| {PARAM_2_NAME} | {P2_OPTIMAL} | {P2_MINUS_20} | {P2_MINUS_10} | {P2_PLUS_10} | {P2_PLUS_20} | {P2_SENSITIVITY} |
| {PARAM_3_NAME} | {P3_OPTIMAL} | {P3_MINUS_20} | {P3_MINUS_10} | {P3_PLUS_10} | {P3_PLUS_20} | {P3_SENSITIVITY} |
| {PARAM_4_NAME} | {P4_OPTIMAL} | {P4_MINUS_20} | {P4_MINUS_10} | {P4_PLUS_10} | {P4_PLUS_20} | {P4_SENSITIVITY} |

**Sensitivity Legend:** Low = robust, Medium = monitor, High = fragile (overfitting risk)

### Overfitting Assessment
- **Parameter Count:** {PARAM_COUNT}
- **Trades per Parameter:** {TRADES_PER_PARAM}
- **Minimum Recommended:** 50 trades per parameter
- **Overfitting Risk:** {OVERFIT_RISK} (Low / Medium / High)

---

## 6. Final Verdict

### Scorecard

| Category | Score (1-10) | Weight | Weighted Score |
|---|---|---|---|
| OOS Performance | {SCORE_OOS} | 25% | {WEIGHTED_OOS} |
| Walk-Forward Results | {SCORE_WF} | 25% | {WEIGHTED_WF} |
| Monte Carlo Robustness | {SCORE_MC} | 20% | {WEIGHTED_MC} |
| Parameter Stability | {SCORE_PARAM} | 15% | {WEIGHTED_PARAM} |
| Prop Firm Viability | {SCORE_PROP} | 15% | {WEIGHTED_PROP} |
| **Total** | | **100%** | **{TOTAL_SCORE}** |

### Verdict Thresholds
- **PASS:** Total score >= 7.0 with no category below 5.0
- **MARGINAL:** Total score 5.0-6.9 or any category below 5.0
- **FAIL:** Total score < 5.0 or any critical category below 3.0

### **OVERALL VERDICT: {FINAL_VERDICT}** (PASS / MARGINAL / FAIL)

### Verdict Notes
{VERDICT_NOTES}

---

## 7. Forward Testing Baseline

### Baseline Metrics (for live comparison)

| Metric | Baseline Value | Alert Threshold (Yellow) | Alert Threshold (Red) |
|---|---|---|---|
| Win Rate | {BL_WIN_RATE}% | < {BL_WR_YELLOW}% | < {BL_WR_RED}% |
| Profit Factor | {BL_PF} | < {BL_PF_YELLOW} | < {BL_PF_RED} |
| Expectancy (R) | {BL_EXPECTANCY}R | < {BL_EXPECT_YELLOW}R | < {BL_EXPECT_RED}R |
| Avg Winner (R) | {BL_AVG_WIN}R | < {BL_AVG_WIN_YELLOW}R | < {BL_AVG_WIN_RED}R |
| Avg Loser (R) | {BL_AVG_LOSS}R | > {BL_AVG_LOSS_YELLOW}R | > {BL_AVG_LOSS_RED}R |
| Max Drawdown ($) | ${BL_MAX_DD} | > ${BL_DD_YELLOW} | > ${BL_DD_RED} |
| Max Consecutive Losses | {BL_MAX_CONSEC_LOSS} | > {BL_CONSEC_YELLOW} | > {BL_CONSEC_RED} |
| Trades per Day | {BL_TRADES_DAY} | < {BL_TRADES_YELLOW} | < {BL_TRADES_RED} |

### Minimum Sample Size for Evaluation
- **Trades Required:** {MIN_EVAL_TRADES}
- **Days Required:** {MIN_EVAL_DAYS}
- **Review Checkpoints:** {EVAL_CHECKPOINTS}

### Forward Test Protocol
1. Trade minimum {MIN_EVAL_TRADES} trades before evaluating
2. Compare all metrics against baseline thresholds
3. If any metric hits RED threshold, halt and investigate
4. If YELLOW threshold hit, continue with heightened monitoring
5. Full evaluation after {MIN_EVAL_DAYS} trading days

---

*Generated: {GENERATED_TIMESTAMP}*
*Backtest report version: 1.0*
*Tool: {BACKTEST_TOOL}*
