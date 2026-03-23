# Automated Trade Execution Research (March 2026)

## Executive Summary

This document covers all viable methods for programmatically executing trades on a Lucid Trading prop firm futures account. The research confirms that **Lucid Trading DOES allow automated trading** (with restrictions), and there are multiple viable paths to execution.

**Best options ranked by feasibility:**
1. **Third-party middleware** (TradersPost / PickMyTrade) -- easiest, most reliable
2. **Direct Tradovate API** via Python -- most flexible, moderate complexity
3. **Direct Rithmic API** via Python -- fastest execution, highest complexity
4. **Custom webhook server** (TradingView -> Python -> Tradovate API) -- full control
5. **TradingView webhooks to middleware** -- simplest if using TradingView signals

---

## 1. Lucid Trading Automation Policy (CRITICAL)

### What's Allowed
- Automated trading systems and trade copiers are **PERMITTED**
- Expert Advisors (EAs) and algorithmic strategies are **PERMITTED**
- Integration with TradersPost and PickMyTrade is **PERMITTED**
- API access via Tradovate and Rithmic is **PERMITTED**

### What's Prohibited
- High-frequency trading (HFT) bots -- **PROHIBITED**
- Latency arbitrage -- **PROHIBITED**
- Multi-account hedging -- **PROHIBITED**

### Key Restrictions
- All trades must be held for **at least 5 seconds**
- At least **50% of profits** must come from trades held longer than 5 seconds
- Daily Loss Limit (DLL) must be monitored manually -- TradingView won't enforce it
- EOD Trailing Max Loss must be monitored manually
- 4:45 PM ET hard close -- positions auto-liquidated
- Consistency rule: largest winning day cannot exceed 20% of cycle profits
- **Traders bear full responsibility for software errors or malfunctions**

### Source
- [Lucid Trading Permitted Activities](https://support.lucidtrading.com/en/articles/11404728-permitted-activities)
- [Lucid Trading Permitted Strategies](https://www.proptradingvibes.com/blog/lucid-trading-permitted-strategies)

---

## 2. TradingView API for Order Execution

### Does TradingView Have a Public Trading API?
**NO.** TradingView does NOT have a public REST API that individual traders can use to place orders. Their APIs are strictly for:

1. **Broker Integration API** -- For brokers (like Tradovate) to integrate with TradingView's platform. This is a server-side REST API that brokers implement, not something traders call.
2. **Charting Library API** -- For licensed partners embedding TradingView charts in their own platforms.

### What This Means
- You CANNOT call a TradingView API endpoint to place a trade
- You CANNOT programmatically interact with TradingView's order panel
- The only programmatic output from TradingView is **outbound webhooks** from alerts

### Feasibility: NOT FEASIBLE for direct order placement
### Source
- [TradingView Broker Integration](https://www.tradingview.com/brokerage-integration/)
- [TradingView API Support Article](https://www.tradingview.com/support/solutions/43000474413-i-need-access-to-your-api-in-order-to-get-data-or-indicator-values/)

---

## 3. TradingView Webhooks

### How They Work
- TradingView sends **outbound** HTTP POST requests when alerts trigger
- Webhooks are ONE-WAY: TradingView -> Your server
- You CANNOT send a webhook TO TradingView to trigger a trade
- Requires TradingView **paid plan** (Essential/Pro or above)
- Requires **2-factor authentication** enabled on TradingView account

### Webhook Architecture
```
TradingView Alert Triggers
    -> HTTP POST to your webhook URL (JSON payload)
    -> Your Python server receives it
    -> Your server calls broker API to execute trade
```

### Limitations
- Remote server must respond within **3 seconds** or request is cancelled
- Alert message max size limitations apply
- Webhook URL must be HTTPS
- No retry mechanism if your server is down

### Feasibility: VIABLE (as signal source, not execution)
### Cost: TradingView Pro/Pro+/Premium ($12.95-$49.95/month)
### Source
- [TradingView Webhook Configuration](https://www.tradingview.com/support/solutions/43000529348-about-webhooks/)

---

## 4. Pine Script Strategy Auto-Execution

### Can Pine Script auto-execute through a connected broker?
**NO.** As of March 2026, TradingView Pine Script strategies are **backtesting only**. There is no native auto-execution of strategy orders through connected brokers.

### Workaround
1. Create a Pine Script strategy/indicator
2. Set up alerts on the strategy signals
3. Configure webhooks on those alerts
4. Route webhooks to a third-party execution service or your own server

### Feasibility: NOT FEASIBLE natively; requires webhook + middleware
### Source
- [TradingView Autotrading Guide](https://www.tradingview.com/support/solutions/43000481026-how-to-autotrade-using-pine-script-strategies/)

---

## 5. Third-Party Middleware Services

### Option A: TradersPost
**What it does:** Receives webhooks from TradingView/TrendSpider/Python and routes orders to connected brokers including Tradovate.

**Pricing:**
| Plan | Monthly | Live Accounts | Asset Classes |
|------|---------|---------------|---------------|
| Starter | $49/mo | 1 | 1 |
| Basic | $99/mo | 2 | 2 |
| Pro | $199/mo | 3 | 3 |
| Premium | $299/mo | 6 | All |
| Extra live accounts | +$10/mo each | | |

**Key Features:**
- Direct Tradovate integration
- Direct Lucid Trading integration (listed as supported prop firm)
- Accepts webhooks from TradingView, TrendSpider, or custom Python scripts
- JSON webhook format for signal submission
- Paper trading available for testing
- Parallel account execution

**Feasibility:** HIGHLY VIABLE -- Purpose-built for this use case
**Source:** [TradersPost Pricing](https://traderspost.io/pricing) | [TradersPost Lucid Trading](https://traderspost.io/connections/lucid-trading)

---

### Option B: PickMyTrade
**What it does:** Cloud-based automation that connects TradingView strategies to Tradovate, Rithmic, and 9+ other brokers.

**Pricing:** $50/month flat -- unlimited strategies, unlimited trades, unlimited accounts

**Key Features:**
- Supports Tradovate AND Rithmic (both Lucid Trading connection types)
- Supports ProjectX
- No WebAPI required on the broker side
- No credit card for 5-day free trial
- Cloud-based -- no need to keep browser open
- Master signal execution across multiple accounts
- Quantity multipliers for position sizing

**Feasibility:** HIGHLY VIABLE -- Best value for prop firm traders
**Source:** [PickMyTrade](https://pickmytrade.trade/) | [PickMyTrade Pricing](https://pickmytrade.io/)

---

### Option C: Other Services
- **AlertDragon** -- TradingView alerts to Tradovate ([alertdragon.com](https://www.alertdragon.com/))
- **Copygram** -- TradingView to Tradovate trade copier ([copygram.app](https://copygram.app/tradingview-to-tradovate))
- **WunderTrading** -- TradingView automation ([wundertrading.com](https://wundertrading.com/en/tradingview-automated-trading))
- **NextLevelBot** -- TradingView automation ([nextlevelbot.com](https://nextlevelbot.com/))
- **PineConnector** -- TradingView to MetaTrader (not relevant for futures)

---

## 6. Direct Tradovate API (BYPASS TradingView)

### Overview
Tradovate provides a full REST + WebSocket API for programmatic trading. This is the **most powerful option** because it lets Python place orders directly without TradingView in the loop at all.

### API Architecture
- **REST API** for authentication, order placement, account management
- **WebSocket API** for real-time data and order updates
- **Demo base URL:** `https://demo.tradovateapi.com/v1`
- **Live base URL:** `https://live.tradovateapi.com/v1`

### Key Endpoints
```
POST /auth/accesstokenrequest  -- Get access token
GET  /account/list             -- List accounts
POST /order/placeorder         -- Place a single order
POST /order/placeOSO           -- Place OCO bracket order (entry + SL + TP)
POST /order/modifyorder        -- Modify existing order
POST /order/cancelorder        -- Cancel an order
GET  /position/list            -- Get open positions
GET  /fill/list                -- Get fill history
```

### Authentication
```python
# Authentication payload
{
    "name": "your_username",
    "password": "your_password",
    "appId": "your_app_name",
    "appVersion": "1.0",
    "cid": "your_client_id",
    "sec": "your_secret_key"
}
```

### Setup Requirements
1. Enable API Access in Tradovate Settings -> Add-Ons ($25/month)
2. Generate API Key (yields Client ID + Secret)
3. Generate a Device ID (unique per machine)
4. Set `isAutomated: true` on all orders (CME Group regulation)

### Cost Breakdown
| Item | Cost |
|------|------|
| Tradovate API Subscription | $25/month |
| CME Market Data (via API) | $290-$390/month (Non-Display Category A) |
| CME Market Data (order-only, no data) | **FREE** -- confirmed by Tradovate staff |

**IMPORTANT:** If you only need to PLACE ORDERS via the API and get market data from TradingView or another source, you do NOT need the CME Non-Display license. Tradovate staff confirmed: "You should be able to send trades without a CME ILA no problem."

### Python Libraries
1. **Tradovate-Python-Client** ([GitHub](https://github.com/cullen-b/Tradovate-Python-Client))
   - Ready-made scripts: PlaceMarketOrder.py, PlaceLimitOrder.py, PlaceTrailStop.py, CancelOrder.py
   - `live` boolean parameter switches between demo/live
   - MIT License

2. **Custom implementation** using `requests` + `websockets` libraries

### Example Pipeline: TradingView Alert -> Python -> Tradovate
```
TradingView Pine Script Alert fires
    -> Webhook POST to your Python Flask server
    -> Python parses JSON (symbol, side, qty, SL, TP)
    -> Python authenticates with Tradovate API
    -> Python calls /order/placeOSO with bracket order
    -> Tradovate executes on Lucid Trading account
    -> Python sends Telegram/Discord confirmation
```

### AWS Lambda Implementation (Proven Architecture)
A proven implementation uses:
- TradingView alert with JSON payload (symbol, side, qty, price, ATR)
- AWS API Gateway receives the webhook
- AWS Lambda function processes the signal
- Lambda authenticates with Tradovate and places OCO order
- CloudWatch for logging, Telegram for notifications

### Feasibility: HIGHLY VIABLE
### Total Cost: $25/month (API only) or $0 if using middleware instead
### Source
- [Tradovate API](https://api.tradovate.com/)
- [Tradovate Python Client](https://github.com/cullen-b/Tradovate-Python-Client)
- [Tradovate API FAQ](https://github.com/tradovate/example-api-faq)
- [CME Fee Not Required for Orders](https://community.tradovate.com/t/is-the-cme-sub-vendor-subscription-required-just-to-send-orders/7793)

---

## 7. Direct Rithmic API (BYPASS TradingView)

### Overview
Rithmic provides the fastest execution available (sub-millisecond) with direct market access to CME, CBOT, NYMEX. Only available on **LucidBlack** accounts (LucidFlex does NOT support Rithmic).

### API Architecture
Rithmic uses Protocol Buffers over WebSockets with 4 separate "plants":
- **TICKER_PLANT** -- Live tick data
- **HISTORY_PLANT** -- Historical data
- **ORDER_PLANT** -- Order management
- **PNL_PLANT** -- P&L updates

Each plant requires its own WebSocket connection and separate login.

### Python Libraries

**1. async_rithmic** ([PyPI](https://pypi.org/project/async-rithmic/)) ([Docs](https://async-rithmic.readthedocs.io/))
```bash
pip install async_rithmic
```
- Python 3.10+ required
- Async-first architecture
- Full order management: submit_order(), cancel_order(), modify_order(), exit_position()
- Supports MARKET, LIMIT, STOP LMT order types
- Auto-reconnection with backoff
- MIT License

**Order Placement Example:**
```python
from async_rithmic import RithmicClient, OrderType

client = RithmicClient(...)
await client.connect()

# Place a market order
await client.submit_order(
    order_id="my_order_1",
    security_code="NQ",
    exchange="CME",
    quantity=1,
    order_type=OrderType.MARKET,
    stop_ticks=20,    # optional SL
    target_ticks=40   # optional TP
)

# Cancel an order
await client.cancel_order(order_id="my_order_1")

# Exit all positions
await client.exit_position()
```

**2. pyrithmic** ([GitHub](https://github.com/jacksonwoody/pyrithmic))
- Another Python implementation of Rithmic Protocol Buffer API
- Asyncio-based
- Supports order placement for futures

### Requirements
- Rithmic API credentials (provided by broker/prop firm)
- R | API+ license (check with Lucid Trading if included with LucidBlack)
- Python 3.10+

### Feasibility: VIABLE (LucidBlack only, higher complexity)
### Cost: Depends on Rithmic license -- may be included with LucidBlack
### Source
- [Rithmic APIs](https://www.rithmic.com/apis)
- [async_rithmic Docs](https://async-rithmic.readthedocs.io/)
- [pyrithmic GitHub](https://github.com/jacksonwoody/pyrithmic)

---

## 8. Browser Automation (Selenium/Playwright)

### Concept
Automate the TradingView web interface using browser automation to click buttons and place orders through the connected broker panel.

### Reality Check
- **Fragile** -- TradingView UI changes frequently, breaking selectors
- **Slow** -- Browser automation adds seconds of latency
- **Detectable** -- TradingView can detect and ban automated browser interactions
- **Against TOS** -- Violates TradingView Terms of Service
- **Unreliable** -- Network issues, page load times, DOM changes

### Feasibility: NOT RECOMMENDED -- use API-based approaches instead

---

## 9. Recommended Architecture for Your System

### Option A: Simplest (No Code Required)
```
Your Python Script generates signal
    -> Send webhook POST to TradersPost/PickMyTrade
    -> Middleware routes order to Tradovate
    -> Tradovate executes on Lucid Trading account
```
**Cost:** $49-50/month (middleware) + TradingView plan if using TV signals
**Complexity:** Low
**Reliability:** High

### Option B: Full Control (Custom Python)
```
Your Python Script generates signal
    -> Python authenticates with Tradovate API
    -> Python calls /order/placeOSO directly
    -> Tradovate executes on Lucid Trading account
    -> Python monitors via WebSocket for fills/updates
```
**Cost:** $25/month (Tradovate API) -- no CME fee needed for order-only
**Complexity:** Medium
**Reliability:** High (you control everything)

### Option C: Hybrid (TradingView + Custom Execution)
```
TradingView Pine Script fires alert
    -> Webhook to your Python Flask/FastAPI server
    -> Python processes signal + risk management
    -> Python calls Tradovate API to execute
    -> Confirmation via Telegram/Discord
```
**Cost:** $25/month (API) + $12.95+/month (TradingView plan)
**Complexity:** Medium
**Reliability:** High

### Option D: Maximum Speed (Rithmic Direct)
```
Your Python Script generates signal
    -> async_rithmic connects to Rithmic ORDER_PLANT
    -> Submit order with sub-millisecond execution
    -> Monitor fills via WebSocket
```
**Cost:** Rithmic license (check with Lucid), LucidBlack account required
**Complexity:** High
**Reliability:** Highest

---

## 10. Key Decision Factors

| Factor | TradersPost/PickMyTrade | Direct Tradovate API | Direct Rithmic API |
|--------|------------------------|---------------------|-------------------|
| Setup time | Minutes | Hours-Days | Days-Weeks |
| Coding required | None/Minimal | Moderate | Advanced |
| Monthly cost | $49-50 | $25 | Varies |
| Execution speed | Fast | Fast | Fastest (<0.5ms) |
| Customization | Limited | Full | Full |
| Reliability | High (managed) | High (you manage) | Highest |
| Risk management | Basic | Full control | Full control |
| Multi-account | Yes | Yes (custom) | Yes (custom) |
| Lucid account type | LucidFlex or Black | LucidFlex or Black | LucidBlack only |

---

## 11. Compliance Checklist for Lucid Trading Automation

- [ ] All trades held minimum 5 seconds
- [ ] 50%+ of profits from trades held >5 seconds
- [ ] `isAutomated: true` flag on all Tradovate API orders (CME requirement)
- [ ] Monitor Daily Loss Limit manually (not enforced by TradingView)
- [ ] Monitor EOD Trailing Max Loss manually
- [ ] Close all positions before 4:45 PM ET
- [ ] No latency arbitrage strategies
- [ ] No HFT patterns
- [ ] No multi-account hedging
- [ ] Consistency rule: largest winning day < 20% of cycle profits
- [ ] Software error responsibility acknowledged

---

## Sources

### Lucid Trading
- [Lucid Trading Official](https://lucidtrading.com/)
- [Lucid Permitted Activities](https://support.lucidtrading.com/en/articles/11404728-permitted-activities)
- [Lucid Permitted Strategies](https://www.proptradingvibes.com/blog/lucid-trading-permitted-strategies)
- [Lucid + TradingView Setup Guide](https://www.proptradingvibes.com/blog/lucid-trading-tradingview)
- [Lucid Supported Platforms](https://support.lucidtrading.com/en/articles/11404614-supported-platforms)

### Tradovate API
- [Tradovate API Documentation](https://api.tradovate.com/)
- [Tradovate API Access](https://support.tradovate.com/s/article/Tradovate-API-Access?language=en_US)
- [Tradovate Python Client](https://github.com/cullen-b/Tradovate-Python-Client)
- [Tradovate API FAQ](https://github.com/tradovate/example-api-faq)
- [CME Fee Not Required for Orders Only](https://community.tradovate.com/t/is-the-cme-sub-vendor-subscription-required-just-to-send-orders/7793)
- [Tradovate API Auth Flow](https://community.tradovate.com/t/what-is-the-correct-auth-flow-to-place-orders/5751)

### Rithmic API
- [Rithmic APIs](https://www.rithmic.com/apis)
- [async_rithmic PyPI](https://pypi.org/project/async-rithmic/)
- [async_rithmic Documentation](https://async-rithmic.readthedocs.io/)
- [async_rithmic GitHub](https://github.com/rundef/async_rithmic)
- [pyrithmic GitHub](https://github.com/jacksonwoody/pyrithmic)

### Third-Party Middleware
- [TradersPost](https://traderspost.io/)
- [TradersPost Pricing](https://traderspost.io/pricing)
- [TradersPost Lucid Trading](https://traderspost.io/connections/lucid-trading)
- [PickMyTrade](https://pickmytrade.trade/)
- [PickMyTrade Prop Firms](https://pickmytrade.io/use-cases/prop-firm-traders)
- [AlertDragon](https://www.alertdragon.com/)

### TradingView
- [TradingView Webhooks](https://www.tradingview.com/support/solutions/43000529348-about-webhooks/)
- [TradingView Autotrading Guide](https://www.tradingview.com/support/solutions/43000481026-how-to-autotrade-using-pine-script-strategies/)
- [TradingView Broker Integration](https://www.tradingview.com/brokerage-integration/)

### Architecture Examples
- [TradingView -> AWS Lambda -> Tradovate](https://www.tradingview.com/chart/NQ1!/3e8S7DB6-Automated-Execution-TradingView-Alerts-Tradovate-using-AWS-La/)
- [TradingView Webhook Trading Bot (Flask)](https://github.com/lth-elm/tradingview-webhook-trading-bot)
- [QuantVPS Best Futures APIs 2026](https://www.quantvps.com/blog/best-apis-for-automated-futures-trading)
