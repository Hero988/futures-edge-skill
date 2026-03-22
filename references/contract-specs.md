# Futures Contract Specifications Reference
last_verified: 2026-03-22

## Overview

This reference covers the specifications for all commonly traded CME Group futures contracts relevant to prop firm trading. Use this for position sizing, tick value calculations, and session planning.

---

## Contract Specifications Table

### E-mini and Micro E-mini Index Futures

| Spec              | ES (E-mini S&P) | MES (Micro S&P) | NQ (E-mini Nasdaq) | MNQ (Micro Nasdaq) |
|-------------------|------------------|------------------|---------------------|---------------------|
| Full Name         | E-mini S&P 500   | Micro E-mini S&P 500 | E-mini Nasdaq-100 | Micro E-mini Nasdaq-100 |
| Exchange          | CME              | CME              | CME                 | CME                 |
| TradingView Symbol| ES1!             | MES1!            | NQ1!                | MNQ1!               |
| Tick Size         | 0.25 points      | 0.25 points      | 0.25 points         | 0.25 points         |
| Tick Value        | $12.50           | $1.25            | $5.00               | $0.50               |
| Point Value       | $50.00           | $5.00            | $20.00              | $2.00               |
| RTH Hours (ET)    | 9:30 AM - 4:00 PM | 9:30 AM - 4:00 PM | 9:30 AM - 4:00 PM | 9:30 AM - 4:00 PM |
| ETH Hours (ET)    | 6:00 PM - 5:00 PM (next day) | Same | Same | Same |
| Rollover Months   | H, M, U, Z       | H, M, U, Z      | H, M, U, Z         | H, M, U, Z         |
| Micro Equivalent  | 10 MES = 1 ES    | --               | 10 MNQ = 1 NQ      | --                  |
| Avg Daily Range   | 40-60 points     | 40-60 points     | 150-250 points      | 150-250 points      |
| Best Trading Time | 9:30-11:30 AM ET | Same             | 9:30-11:00 AM ET   | Same                |

### Dow and Russell Index Futures

| Spec              | YM (E-mini Dow)  | MYM (Micro Dow)  | RTY (E-mini Russell) | M2K (Micro Russell) |
|-------------------|------------------|-------------------|----------------------|----------------------|
| Full Name         | E-mini Dow Jones  | Micro E-mini Dow  | E-mini Russell 2000  | Micro E-mini Russell 2000 |
| Exchange          | CBOT             | CBOT              | CME                  | CME                  |
| TradingView Symbol| YM1!             | MYM1!             | RTY1!                | M2K1!                |
| Tick Size         | 1.00 points      | 1.00 points       | 0.10 points          | 0.10 points          |
| Tick Value        | $5.00            | $0.50             | $5.00                | $0.50                |
| Point Value       | $5.00            | $0.50             | $50.00               | $5.00                |
| RTH Hours (ET)    | 9:30 AM - 4:00 PM | 9:30 AM - 4:00 PM | 9:30 AM - 4:00 PM | 9:30 AM - 4:00 PM |
| ETH Hours (ET)    | 6:00 PM - 5:00 PM (next day) | Same | Same | Same |
| Rollover Months   | H, M, U, Z       | H, M, U, Z       | H, M, U, Z          | H, M, U, Z          |
| Micro Equivalent  | 10 MYM = 1 YM    | --                | 10 M2K = 1 RTY      | --                   |
| Avg Daily Range   | 300-500 points   | 300-500 points    | 15-25 points         | 15-25 points         |
| Best Trading Time | 9:30-11:00 AM ET | Same              | 9:30-11:00 AM ET    | Same                 |

### Energy and Metals Futures

| Spec              | CL (Crude Oil)   | MCL (Micro Crude) | GC (Gold)          | MGC (Micro Gold)   |
|-------------------|------------------|--------------------|--------------------|---------------------|
| Full Name         | WTI Crude Oil     | Micro WTI Crude    | Gold Futures       | Micro Gold Futures  |
| Exchange          | NYMEX            | NYMEX              | COMEX              | COMEX               |
| TradingView Symbol| CL1!             | MCL1!              | GC1!               | MGC1!               |
| Tick Size         | 0.01 ($0.01/bbl) | 0.01               | 0.10 ($0.10/oz)    | 0.10                |
| Tick Value        | $10.00           | $1.00              | $10.00             | $1.00               |
| Point Value       | $1,000.00        | $100.00            | $100.00            | $10.00              |
| RTH Hours (ET)    | 9:00 AM - 2:30 PM | 9:00 AM - 2:30 PM | 8:20 AM - 1:30 PM | 8:20 AM - 1:30 PM |
| ETH Hours (ET)    | 6:00 PM - 5:00 PM (next day) | Same | Same | Same |
| Rollover Months   | Monthly (F-Z)    | Monthly (F-Z)     | G, J, M, Q, V, Z  | G, J, M, Q, V, Z   |
| Micro Equivalent  | 10 MCL = 1 CL    | --                 | 10 MGC = 1 GC     | --                  |
| Avg Daily Range   | $1.50-$3.00      | $1.50-$3.00       | $20-$40            | $20-$40             |
| Best Trading Time | 9:00-10:30 AM ET | Same               | 8:30-10:00 AM ET  | Same                |

---

## Rollover Calendar

### Rollover Month Codes
| Code | Month     |
|------|-----------|
| F    | January   |
| G    | February  |
| H    | March     |
| J    | April     |
| K    | May       |
| M    | June      |
| N    | July      |
| Q    | August    |
| U    | September |
| V    | October   |
| X    | November  |
| Z    | December  |

### Quarterly Index Futures Rollover (ES, NQ, YM, RTY and micros)
- **Rollover months**: March (H), June (M), September (U), December (Z)
- **Rollover date**: Second Thursday of the expiration month (typically 8 days before expiration)
- **Expiration**: Third Friday of the expiration month
- **Volume shifts**: Most volume moves to the next contract 7-10 days before expiration

### 2026 Quarterly Rollover Dates (Approximate)
| Quarter | Contract Expiry | Rollover Date (Volume Shift) | New Front Month |
|---------|----------------|------------------------------|-----------------|
| Q1 2026 | Mar 20, 2026   | ~Mar 12, 2026                | June (M) 2026   |
| Q2 2026 | Jun 19, 2026   | ~Jun 11, 2026                | Sept (U) 2026   |
| Q3 2026 | Sep 18, 2026   | ~Sep 10, 2026                | Dec (Z) 2026    |
| Q4 2026 | Dec 18, 2026   | ~Dec 10, 2026                | Mar (H) 2027    |

### Crude Oil (CL) Rollover
- Monthly contracts. Each month has its own contract.
- Expiration: ~3 business days before the 25th of the month prior to delivery month
- Volume typically shifts 3-5 days before expiration
- Example: CL April (CLJ26) expires around March 20, 2026. Volume shifts to May (CLK26) around March 17.

### Gold (GC) Rollover
- Active months: February (G), April (J), June (M), August (Q), October (V), December (Z)
- Expiration: Third-to-last business day of the month prior to delivery
- Volume typically shifts 5-7 days before expiration

---

## Continuous Contracts on TradingView

### How They Work
- **ES1!** = Front month (most active) continuous contract. Automatically rolls to next active contract.
- **ESH2026** = Specific contract (March 2026 E-mini S&P). Does not roll.
- **ES2!** = Second month continuous contract.

### Which to Use
- For charting and analysis: Use **ES1!** (continuous front month) for clean charts
- For actual trading: Know which specific contract month you are trading (e.g., ESM2026 for June 2026)
- Backtesting: Use continuous contracts but be aware of rollover gaps

### Rollover Gap
- When continuous contracts roll, there can be a price gap between the old and new contract
- This gap is NOT a tradeable gap -- it is an artifact of the contract change
- Some platforms adjust for this (back-adjusted data), some do not
- For daily charts spanning rollovers, use back-adjusted continuous contracts

---

## Quick Reference: Position Sizing Cheat Sheet

| Contract | 1 Tick Value | 10 Tick Stop Cost | 20 Tick Stop Cost | Contracts for $500 Risk (10-tick stop) |
|----------|-------------|-------------------|-------------------|----------------------------------------|
| ES       | $12.50      | $125.00           | $250.00           | 4                                      |
| MES      | $1.25       | $12.50            | $25.00            | 40                                     |
| NQ       | $5.00       | $50.00            | $100.00           | 10                                     |
| MNQ      | $0.50       | $5.00             | $10.00            | 100                                    |
| YM       | $5.00       | $50.00            | $100.00           | 10                                     |
| MYM      | $0.50       | $5.00             | $10.00            | 100                                    |
| RTY      | $5.00       | $50.00            | $100.00           | 10                                     |
| M2K      | $0.50       | $5.00             | $10.00            | 100                                    |
| CL       | $10.00      | $100.00           | $200.00           | 5                                      |
| MCL      | $1.00       | $10.00            | $20.00            | 50                                     |
| GC       | $10.00      | $100.00           | $200.00           | 5                                      |
| MGC      | $1.00       | $10.00            | $20.00            | 50                                     |

---

## Commission Reference (Typical)

| Contract Type | Round-Trip Commission | Notes                            |
|---------------|----------------------|----------------------------------|
| Standard (ES, NQ, etc.) | $4.00 - $5.50 | Varies by broker/platform |
| Micro (MES, MNQ, etc.)  | $1.00 - $2.50 | Some prop firms include in fees |
| CL                       | $4.00 - $5.50 | Same as standard index          |
| GC                       | $4.00 - $5.50 | Same as standard index          |

Note: Prop firm simulated accounts may not charge commissions separately (often included in the spread or platform fee). Check your specific firm.
