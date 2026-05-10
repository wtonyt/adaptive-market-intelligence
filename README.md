# NodeAsset CoPilot

This repository is the reference CoPilot analysis worker for NodeAsset. It may still be named `market-ml-databricks` in source control, but the product role is **NodeAsset CoPilot**: a customer-side reasoning service that reviews subscribed RL/ML specialist trades and returns human-trader analysis to NodeAsset Terminal.

CoPilot is not an autonomous execution agent. Its job is to help traders understand whether a NodeAsset opportunity is approaching, still timely, stale, risky, or worth watching.

## What CoPilot Does

When a subscribed NodeAsset specialist trade arrives, CoPilot:

- receives an analysis request from `nodeasset-openclaw-trader`,
- evaluates the trade using the local reasoning layer,
- classifies the setup for human review,
- posts the analysis back to NodeAsset API,
- lets NodeAsset Terminal show the findings in the `CoPilot` screen.

The output is persisted by NodeAsset API and can be reviewed later.

```text
NodeAsset API
  subscribed RL/ML specialist trade
        |
        v
nodeasset-openclaw-trader
  verifies and forwards CoPilot request
        |
        v
NodeAsset CoPilot
  analyzes trade and posts findings
        |
        v
NodeAsset API
  stores copilot_trade_analyses
        |
        v
NodeAsset Terminal
  CoPilot screen + trade-specific chat
```

## Required Services

To enable CoPilot for a tenant or customer account, run these services:

- **NodeAsset API**: owns subscriptions, trade entitlement, persisted CoPilot findings, and Terminal APIs.
- **NodeAsset Terminal**: displays the `CoPilot` menu, analysis queue, reasons, risks, and chat.
- **nodeasset-openclaw-trader**: receives NodeAsset events and forwards CoPilot analysis requests.
- **NodeAsset CoPilot**: this service; performs the analysis and calls back to NodeAsset API.

Install the OpenClaw bridge first:

```bash
git clone https://github.com/nodeassetcorp/nodeasset-openclaw-trader.git
```

## Enablement Checklist

1. Confirm the customer has active NodeAsset specialist subscriptions.
2. Deploy or run NodeAsset API with CoPilot endpoints enabled.
3. Deploy NodeAsset Terminal with the `CoPilot` menu enabled.
4. Install and configure `nodeasset-openclaw-trader`.
5. Run this CoPilot service.
6. Configure shared event tokens between services.
7. Trigger a test trade or webhook test.
8. Confirm Terminal shows a CoPilot record moving from `pending` or `processing` to `ready`.

## Service Configuration

### NodeAsset API

NodeAsset API should know where to send CoPilot analysis requests:

```text
COPILOT_ANALYSIS_URL=http://nodeasset-openclaw-trader:8080/events/nodeasset-copilot-analysis
COPILOT_ANALYSIS_TOKEN=replace-with-shared-token
COPILOT_CHAT_URL=http://nodeasset-copilot:8000/events/openclaw/copilot-chat
```

NodeAsset API receives completed findings at:

```text
POST /gappers/copilot/analysis-results
```

The callback is protected by `COPILOT_ANALYSIS_TOKEN` or `COPILOT_RESULT_TOKEN`.

### nodeasset-openclaw-trader

The OpenClaw bridge should forward normal trade events and CoPilot analysis requests separately:

```text
FORWARD_URL=http://nodeasset-copilot:8000/events/openclaw/nodeasset-trade
FORWARD_TOKEN=replace-with-shared-token

COPILOT_FORWARD_URL=http://nodeasset-copilot:8000/events/openclaw/copilot-analysis
COPILOT_FORWARD_TOKEN=replace-with-shared-token
```

### NodeAsset CoPilot

This service verifies requests and posts findings back to NodeAsset API:

```text
EVENT_INGEST_TOKEN=replace-with-shared-token
NODEASSET_COPILOT_RESULT_URL=https://api.nodeasset.com/gappers/copilot/analysis-results
NODEASSET_COPILOT_RESULT_TOKEN=replace-with-shared-token
```

Local defaults are in `docker-compose.yml`.

## CoPilot Endpoints

### Analyze A Trade

`nodeasset-openclaw-trader` calls:

```text
POST /events/openclaw/copilot-analysis
```

Example request:

```json
{
  "type": "nodeasset.copilot.analysis.requested",
  "event_id": "customer@example.com:trd_01:analysis",
  "user_email": "customer@example.com",
  "data": {
    "trade_id": "trd_01",
    "specialist": "runner",
    "symbol": "NVDA",
    "side": "BUY",
    "quantity": 10,
    "price": 915.25,
    "timestamp": "2026-05-11T14:35:00Z"
  }
}
```

Example response:

```json
{
  "status": "ready",
  "mode": "openclaw-copilot",
  "callback_sent": true,
  "analysis": {
    "trade_id": "trd_01",
    "actionability": "strong_watch",
    "summary": "runner BUY on NVDA is classified as strong_watch. The review is decision support for a human trader, not an autonomous execution instruction.",
    "confidence_score": 0.79,
    "reasons": [
      "runner issued a BUY signal on NVDA.",
      "Composite confidence is 0.79.",
      "Market regime is UNKNOWN."
    ],
    "risks": [
      "Market regime is unknown because the local candle store does not yet have enough symbol history."
    ],
    "questions": [
      "Is this signal still close to the original price?",
      "How does this compare to recent trades from the same specialist?",
      "What would make this setup stale?"
    ]
  }
}
```

### Answer A Follow-Up Question

NodeAsset API can call:

```text
POST /events/openclaw/copilot-chat
```

The request includes the saved analysis and the trader's question. The response is intentionally simple:

```json
{
  "reply": "The setup is still a watch, but it needs fresh price and volume context before a trader treats it as actionable."
}
```

## What Gets Persisted

NodeAsset API persists customer-facing CoPilot findings in MongoDB:

- `copilot_trade_analyses`
- `copilot_trade_messages`

This service also stores local reasoning records in PostgreSQL:

- `signal_events`
- `consensus_events`
- `market_candles`
- `agent_performance`

NodeAsset API is the source used by Terminal. The local PostgreSQL data is useful for worker diagnostics, replay, and later model analysis.

## Local Run

Start the CoPilot worker and PostgreSQL:

```bash
docker compose up --build api
```

Health check:

```bash
curl http://localhost:8000/
```

Expected:

```json
{
  "status": "running",
  "default_mode": "openclaw",
  "recommended_ingest": "/events/openclaw/nodeasset-trade",
  "fallback_ingest": "/events/nodeasset-trade"
}
```

Manual CoPilot test:

```bash
curl -X POST http://localhost:8000/events/openclaw/copilot-analysis \
  -H "Content-Type: application/json" \
  -H "X-Event-Token: local-openclaw-token" \
  -d '{
    "type": "nodeasset.copilot.analysis.requested",
    "user_email": "customer@example.com",
    "data": {
      "trade_id": "local-test-1",
      "specialist": "runner",
      "symbol": "NVDA",
      "side": "BUY",
      "quantity": 10,
      "price": 915.25,
      "timestamp": "2026-05-11T14:35:00Z"
    }
  }'
```

## Operational Notes

- Run this service continuously if customers expect near real-time CoPilot findings.
- If this service is down, NodeAsset Terminal can still show pending analysis records, but they will not become `ready`.
- Use the same shared token across `COPILOT_ANALYSIS_TOKEN`, `COPILOT_FORWARD_TOKEN`, `EVENT_INGEST_TOKEN`, and `NODEASSET_COPILOT_RESULT_TOKEN` unless a tenant requires separate secrets.
- The current implementation provides deterministic reasoning over the trade and local context. Richer analysis should add tools for live quotes, candles, specialist history, and similar historical trades.
- `UNKNOWN` market regime is normal in a fresh local database until `market_candles` has enough symbol history.

## Positioning

NodeAsset CoPilot is best positioned as:

```text
Real-time reasoning over NodeAsset RL/ML generated trades for human traders.
```

It helps customers understand:

- why a trade matters,
- whether it is still timely,
- what risks are visible,
- what would make it stale,
- what questions to ask before acting.

It should not be marketed as autonomous execution unless a customer explicitly adds and controls execution tooling.

## Future Rename

This repo can be renamed from `market-ml-databricks` to `nodeasset-copilot`. The expected product name in documentation and customer setup is already **NodeAsset CoPilot**.
