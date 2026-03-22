# Prop Firm Rules Reference
last_verified: 2026-03-22

## Overview

This reference covers the rules and specifications for five major futures prop firms. Rules change frequently -- always verify against the firm's official site before trading. This document reflects known rules as of March 2026.

**Important**: All prop firm funded accounts trade simulated markets. Payouts are real, but fills are sim. This means you may experience better fills than live markets.

---

## Topstep

### Account Sizes and Targets

| Parameter            | $50K Account | $100K Account | $150K Account |
|----------------------|-------------|---------------|---------------|
| Profit Target (Eval) | $3,000      | $6,000        | $9,000        |
| Max Drawdown         | $2,000      | $3,000        | $4,500        |
| Daily Loss Limit     | None stated | None stated   | None stated   |
| Max Contracts        | 5 std / 50 micro | 10 std / 100 micro | 15 std / 150 micro |

### Drawdown Type
- **End-of-Day (EOD) Trailing Drawdown**: Drawdown floor moves up based on end-of-day equity, NOT intraday high
- The floor only advances at the session close, giving intraday breathing room
- Floor stops trailing once it reaches the starting account balance (becomes static)
- Example ($50K): Start with floor at $48,000. If you close the day at $51,500, floor moves to $49,500. Once floor reaches $50,000, it locks there permanently.

### Payout Structure
- **90/10 split** (you keep 90%)
- Minimum payout: $50 on TopstepX
- Payouts processed within 1-2 business days
- No minimum trading days before first payout on TopstepX

### Trading Rules
- **Close all positions by 3:10 PM CT** (4:10 PM ET) daily
- **No overnight positions** (no holding through close)
- **News trading allowed**: No restrictions around economic releases
- **Platform**: TopstepX (proprietary) or NinjaTrader for evaluation
- **Scaling plan**: Starts with reduced contracts, scales up as profit grows

### Evaluation Rules
- No minimum trading days
- No maximum time limit to pass
- No consistency rule during evaluation
- Must reach profit target without violating drawdown

### Key Nuances
- Topstep is the most established futures prop firm (since 2012)
- TopstepX platform has built-in risk management that auto-closes positions at drawdown limit
- Multiple account resets available with subscription
- Can hold multiple funded accounts simultaneously

---

## Apex Trader Funding

### Account Sizes (Common)
| Parameter            | $50K Account | $100K Account | $150K Account | $250K Account |
|----------------------|-------------|---------------|---------------|---------------|
| Profit Target (Eval) | $3,000      | $6,000        | $9,000        | $15,000       |
| Trailing Drawdown    | $2,500      | $3,000        | $5,000        | $6,500        |
| Max Contracts        | 4 std       | 10 std        | 12 std        | 16 std        |

### Drawdown Type
- **Two options at purchase**: Trailing drawdown OR End-of-Day drawdown
- Trailing: Floor follows your intraday equity high in real-time (more restrictive)
- EOD: Floor follows end-of-day balance (more forgiving, recommended)
- Choose at account purchase -- cannot change later

### Payout Structure
- **100% of first $25,000** in profits, then **90/10 split**
- Minimum 10 paid days before first withdrawal on PA (Performance Account)
- Two payouts per month maximum
- Minimum payout: $500

### Trading Rules
- **Close all positions by 4:59 PM ET** daily
- **No overnight positions**
- **News trading allowed**: No specific blackout windows
- **Consistency rule (PA)**: 50% rule -- no single trading day can account for more than 50% of total profits (only applies on PA, not during eval)
- **One-time billing model**: As of March 2026, Apex uses one-time fee (no monthly subscription for eval)
- **30-day evaluation limit**: Must pass within 30 calendar days or account expires

### Funded Account (PA) Specifics
- Reduced contract limits compared to evaluation
- Metals (GC, SI) may be suspended or restricted on PA accounts -- check current status
- Scaling plan may apply based on account profit
- Inactivity rule: Must place at least one trade every 7 days

### Key Nuances
- Frequently offers promotional pricing (80-90% off evaluations)
- Large community and social media presence
- Account purchasing through website with many size options
- Can hold up to 20 active evaluation accounts simultaneously

---

## Bulenox

### Account Sizes (Common)
| Parameter            | $25K Account | $50K Account | $100K Account | $150K Account |
|----------------------|-------------|-------------|---------------|---------------|
| Profit Target (Eval) | $1,500      | $3,000      | $6,000        | $9,000        |
| Max Drawdown         | $1,500      | $2,500      | $3,500        | $5,000        |
| Daily Loss Limit     | $500        | $1,100      | $2,000        | $2,500        |
| Max Contracts        | 3 std       | 5 std       | 10 std        | 15 std        |

### Drawdown Type
- **Trailing OR EOD with Daily Loss Limit (DLL)**
- Trailing: Real-time trailing drawdown (most restrictive)
- EOD with DLL: End-of-day drawdown + separate daily loss limit (recommended -- more forgiving overall despite the DLL)
- Choose at account purchase

### Payout Structure
- **100% of first $10,000**, then **90/10 split**
- Weekly payouts processed every Wednesday
- Minimum payout: $100 (after initial minimum trading days)
- No maximum payout cap

### Trading Rules
- **Close all positions by 3:59 PM CST** (4:59 PM ET) daily
- **No overnight positions**
- **Scaling plan required**: Start with reduced contracts, scale up as account grows
- **Consistency rule (funded)**: 40% -- no single day > 40% of total profit
- **Minimum trading days**: 5 trading days in evaluation before qualification

### Funded Account Specifics
- Scaling plan limits initial contract size
- Must maintain the 40% consistency rule throughout funded period
- Inactivity rule: Must trade at least once every 14 calendar days
- Daily loss limit is separate from overall drawdown (can be violated even if drawdown has room)

### Key Nuances
- Monthly subscription model for evaluations
- Competitive pricing, often runs promotions
- Platform: NinjaTrader, Rithmic-connected platforms
- Known for straightforward rules and fast payouts

---

## MyFundedFutures (MFF)

### Account Types

| Parameter            | Starter ($50K) | Core ($100K) | Rapid ($100K) | Pro ($150K) |
|----------------------|----------------|-------------|---------------|-------------|
| Profit Target (Eval) | $3,000         | $6,000      | $4,000        | $9,000      |
| Max Drawdown         | $2,000         | $3,000      | $2,500        | $4,500      |
| Daily Loss Limit     | **None**       | **None**    | **None**      | **None**    |
| Max Contracts        | 3 std          | 10 std      | 10 std        | 15 std      |
| Eval Days Required   | 2 min          | 2 min       | 2 min         | 2 min       |

### Drawdown Type
- **Trailing drawdown** (real-time, follows intraday equity high)
- Drawdown trails until it reaches the starting balance, then becomes static
- No daily loss limit is a major differentiator -- the only limit is the overall drawdown

### Payout Structure
- **Starter/Core**: 80/20 split, upgradeable to 90/10 after consistency
- **Pro**: 90/10 split from the start
- Minimum 2 profitable trading days before first payout request
- Payouts processed within 24-48 hours

### Trading Rules
- **No daily loss limit**: Only overall drawdown matters
- **2-minute news blackout**: Must close all positions 2 minutes before AND 2 minutes after major economic releases (NFP, CPI, FOMC, etc.)
- **Overnight positions ALLOWED**: One of the few firms that permits holding through close (with proper risk management)
- **Consistency rule (eval)**: 50% -- no single day > 50% of profit target during evaluation
- **Minimum 2 trading days** to pass evaluation

### Funded Account Specifics
- **Scaling required (Core/Rapid)**: Start with reduced contracts, scale up based on profit
- **Pro accounts**: No scaling, full contracts from day one
- Overnight positions allowed but count toward drawdown
- News blackout auto-liquidation: Platform will automatically close positions within the 2-min window

### Key Nuances
- No daily loss limit makes MFF unique and popular
- Overnight holding allowed -- good for swing trade strategies
- Rapid account has lower profit target but tighter drawdown
- Strong reputation for fast payouts
- Monthly subscription for evaluations

---

## TradeDay

### Account Sizes (Common)
| Parameter            | $50K Account | $100K Account | $150K Account |
|----------------------|-------------|---------------|---------------|
| Profit Target (Eval) | $3,000      | $6,000        | $9,000        |
| Max Drawdown         | $2,000      | $3,000        | $4,500        |
| Max Contracts        | 5 std       | 10 std        | 15 std        |

### Drawdown Types (Choose One)
- **Intraday Trailing**: Most restrictive. Trails intraday equity high in real-time.
- **End-of-Day (EOD)**: Floor moves based on end-of-day balance. More forgiving.
- **Static Drawdown**: Fixed drawdown from starting balance. Does NOT trail. Most forgiving but typically lower drawdown amount.

### Payout Structure
- **Tiered split**:
  - First $10,000 in profits: 100% to trader
  - $10,001 - $20,000: 95/5 split
  - $20,001+: 95/5 split
- **24-hour payout processing** (one of the fastest)
- Minimum payout: $100

### Trading Rules
- **Close all positions by 3:50 PM CT** (4:50 PM ET)
- **No overnight positions**
- **Consistency rule (eval)**: 30% -- no single day > 30% of total profit during evaluation (most strict consistency rule among the five firms)
- **2-minute news auto-liquidation**: Platform automatically liquidates all positions within 2 minutes of major economic releases
- **Minimum 5 trading days** in evaluation

### Funded Account Specifics
- Metals (GC, SI) may be restricted -- check current rules
- Scaling plan may apply depending on account type
- Consistency rule may continue into funded phase
- Must trade at least once every 5 business days (inactivity rule)

### Key Nuances
- Known for fast payouts (24 hours)
- Static drawdown option is unique and attractive
- 30% consistency rule is the strictest -- be aware during evaluation
- Regular promotional pricing
- Platform: NinjaTrader, Rithmic-connected

---

## Quick Comparison Table

| Feature              | Topstep     | Apex        | Bulenox     | MFF         | TradeDay    |
|----------------------|-------------|-------------|-------------|-------------|-------------|
| Drawdown Type        | EOD Trail   | Trail/EOD   | Trail/EOD+DLL| Trail      | Trail/EOD/Static |
| Daily Loss Limit     | No          | No          | Yes (EOD)   | **No**      | No          |
| Overnight Allowed    | No          | No          | No          | **Yes**     | No          |
| News Restriction     | None        | None        | None        | 2-min       | 2-min auto  |
| Consistency (Eval)   | None        | None        | None        | 50%         | 30%         |
| Consistency (Funded) | None        | 50%         | 40%         | Varies      | Varies      |
| First $X at 100%     | No (90/10)  | $25K (100%) | $10K (100%) | No          | $10K (100%) |
| Ongoing Split        | 90/10       | 90/10       | 90/10       | 80/20-90/10 | 95/5        |
| Payout Speed         | 1-2 days    | 2x/month    | Weekly Wed  | 24-48 hrs   | 24 hrs      |
| Close-By Time (ET)   | 4:10 PM     | 4:59 PM     | 4:59 PM     | None        | 4:50 PM     |
| Min Eval Days        | None        | None        | 5           | 2           | 5           |
| Eval Time Limit      | None        | 30 days     | None        | None        | None        |

---

## Common Rules Across All Firms

### Universal Rules
- **CME Group futures only**: ES, NQ, YM, RTY, CL, GC, SI, and their micros. No forex spot, no crypto spot, no stocks.
- **No hedging across accounts**: Cannot be long ES on one account and short ES on another at the same firm
- **KYC required**: Government ID and proof of address needed before first payout
- **Simulated trading**: All funded accounts are simulated until explicitly stated otherwise. Fills may differ from live markets.
- **One person per account**: Cannot share login or let someone else trade your account
- **No EAs/bots during evaluation** at some firms: Check individual firm rules. Most allow automated trading but some restrict it during eval.

### Best Practices Across All Firms
1. **Choose EOD drawdown** when available (more forgiving than trailing)
2. **Know your close-by time** and set an alarm 15 minutes before
3. **Check the economic calendar daily** for news blackout compliance
4. **Track your consistency ratio** daily if your firm has a consistency rule
5. **Maintain a drawdown buffer** of at least 30% of max drawdown
6. **Start with micro contracts** on funded accounts to build buffer before scaling up
7. **Read the updated rules monthly**: Firms change rules frequently, sometimes without prominent announcement
