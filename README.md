# Market ML Databricks

Market ML Databricks is a customer-side reasoning and analytics application for the NodeAsset subscription system. Customers subscribe to NodeAsset specialists, receive only the trades they are entitled to, and can use this repo to turn those subscribed signals into local decisions, sizing guidance, event logs, and historical feedback.

The default integration mode is OpenClaw.

Install and configure the NodeAsset OpenClaw bridge first:

```text
https://github.com/nodeassetcorp/nodeasset-openclaw-trader
```

This repo expects `nodeasset-openclaw-trader` to already be running and forwarding authenticated NodeAsset trade events. Market ML Databricks is the downstream reasoning app, not the NodeAsset webhook receiver.

For NodeAsset CoPilot, this app also accepts analysis requests from `nodeasset-openclaw-trader`:

```text
POST /events/openclaw/copilot-analysis
```

Set `NODEASSET_COPILOT_RESULT_URL` to the NodeAsset API callback endpoint, usually `/gappers/copilot/analysis-results`, so completed findings can appear in NodeAsset Terminal in near real time.

```text
NodeAsset global trades
        |
        v
NodeAsset subscription filter
        |
        v
nodeasset-openclaw-trader
install first: https://github.com/nodeassetcorp/nodeasset-openclaw-trader
        |
        v
Market ML Databricks reasoning API
        |
        v
PostgreSQL consensus records + JSONL event logs + downstream analytics
```

Direct NodeAsset API polling is still present as a fallback, but it is intentionally de-prioritized. New customer integrations should install [`nodeasset-openclaw-trader`](https://github.com/nodeassetcorp/nodeasset-openclaw-trader) first because it gives the customer a local agent boundary for their own context, tools, policies, and prompts before Market ML persists and evaluates the signal.

## What Happens When Trades Start

When NodeAsset emits a new trade for a subscribed specialist:

1. NodeAsset keeps the trade global and applies subscription entitlement.
2. [`nodeasset-openclaw-trader`](https://github.com/nodeassetcorp/nodeasset-openclaw-trader) receives the entitled trade by webhook push mode or optional pull mode.
3. OpenClaw forwards the event to this app at `/events/openclaw/nodeasset-trade`.
4. This app normalizes the event into a `TraderSignal`.
5. The reasoning layer evaluates confidence, liquidity, timing, market regime, and position sizing.
6. The API returns a final action: `BUY`, `SELL`, `HOLD`, or `SKIP`.
7. The raw event is appended to `data/nodeasset_trades.log`.
8. The reasoned signal and consensus decision are persisted in PostgreSQL.

Example response:

```json
{
  "status": "reasoned",
  "mode": "openclaw",
  "trade_id": "local-test-qa-3",
  "specialist": "runner",
  "symbol": "NVDA",
  "decision": {
    "recommended_action": "BUY",
    "reasoning": {
      "mode": "openclaw",
      "regime": "UNKNOWN",
      "threshold": 0.7,
      "position_percent": 0.1,
      "market_context_score": 0.75
    },
    "consensus": {
      "symbol": "NVDA",
      "rl_side": "BUY",
      "consensus": true,
      "consensus_score": 0.799,
      "final_side": "BUY",
      "confidence_score": 0.799
    }
  }
}
```

`UNKNOWN` market regime is expected in a fresh local Docker database until `market_candles` has enough history for the requested symbol.

## Reasoning Layer

This branch now includes the QA reasoning pieces needed to reason over OpenClaw-forwarded NodeAsset trades:

- `src/services/openclaw_reasoning_engine.py`: turns OpenClaw/NodeAsset events into local decisions.
- `src/services/trade_events.py`: normalizes raw direct/API/OpenClaw event envelopes.
- `src/services/market_regime_engine.py`: classifies the symbol as `TRENDING`, `VOLATILE`, `NEUTRAL`, or `UNKNOWN`.
- `src/services/position_sizing_engine.py`: converts confidence and market regime into a suggested position percentage.
- `src/db/*`: persists signal events, consensus events, market candles, and performance feedback.
- `src/schemas/signals.py`: shared `TraderSignal` and `ConsensusSignal` models.

For OpenClaw events, NodeAsset is treated as the subscribed specialist signal. The reasoning adapter then applies local confidence, liquidity, timing, market regime, and position sizing checks before returning an action.

## OpenClaw Default Path

Install `nodeasset-openclaw-trader` before running this app:

```bash
git clone https://github.com/nodeassetcorp/nodeasset-openclaw-trader.git
cd nodeasset-openclaw-trader
```

Follow that repo's README to configure NodeAsset authentication, webhook signing, and OpenClaw runtime settings. Once the bridge is installed, configure it to forward to this API:

```bash
FORWARD_URL=http://market_ml_api:8000/events/openclaw/nodeasset-trade
FORWARD_TOKEN=replace-with-shared-token
COPILOT_FORWARD_URL=http://market_ml_api:8000/events/openclaw/copilot-analysis
COPILOT_FORWARD_TOKEN=replace-with-shared-token
```

Configure this app with the same token:

```bash
EVENT_INGEST_TOKEN=replace-with-shared-token
```

The token may be sent as:

```text
X-Event-Token: replace-with-shared-token
```

or:

```text
Authorization: Bearer replace-with-shared-token
```

Sample OpenClaw event:

```json
{
  "event": "nodeasset.trade.received",
  "data": {
    "trade_id": "664f2-example",
    "specialist": "runner",
    "symbol": "NVDA",
    "side": "BUY",
    "confidence": 0.82,
    "price": 915.25,
    "timestamp": "2026-05-11T14:35:00Z"
  }
}
```

Manual test:

```bash
curl -X POST http://localhost:8000/events/openclaw/nodeasset-trade \
  -H "Content-Type: application/json" \
  -H "X-Event-Token: local-openclaw-token" \
  -d '{
    "event": "nodeasset.trade.received",
    "data": {
      "trade_id": "local-test-1",
      "specialist": "runner",
      "symbol": "NVDA",
      "side": "BUY",
      "confidence": 0.82,
      "price": 915.25,
      "timestamp": "2026-05-11T14:35:00Z"
    }
  }'
```

## Direct API Fallback

The direct handoff endpoint remains available:

```text
POST /events/nodeasset-trade
```

It runs the same reasoning path and persistence as the OpenClaw endpoint, but it removes the local OpenClaw agent boundary. Use this mainly for internal tests, simple server-to-server integrations, or customers that only need deterministic sizing output from raw subscribed trades.

The older direct poller service is still included:

```bash
docker compose run --rm poller
```

The poller reads from NodeAsset's subscribed-trades API and appends normalized records to `data/nodeasset_trades.log`. It does not replace the preferred OpenClaw path.

## Local Docker Run

Start PostgreSQL and the API:

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

Default local values in `docker-compose.yml`:

```text
EVENT_INGEST_TOKEN=local-openclaw-token
NODEASSET_DEFAULT_CONFIDENCE=0.82
NODEASSET_DEFAULT_LIQUIDITY_SCORE=0.75
NODEASSET_DEFAULT_TIMING_SCORE=0.75
NODEASSET_OPENCLAW_ACTION_THRESHOLD=0.70
NODEASSET_EVENT_LOG=data/nodeasset_trades.log
NODEASSET_REASONED_EVENT_LOG=data/nodeasset_openclaw_reasoned.log
NODEASSET_COPILOT_RESULT_URL=https://api.nodeasset.com/gappers/copilot/analysis-results
NODEASSET_COPILOT_RESULT_TOKEN=replace-with-shared-token
```

## Persistence

PostgreSQL stores the reasoned outputs:

- `signal_events`: normalized NodeAsset specialist signal plus final action.
- `consensus_events`: confidence score, final side, reason, and timestamp.
- `market_candles`: symbol candle history used for regime detection.
- `agent_performance`: feedback records used by adaptive weighting work.

JSON-lines logs are also written for lightweight local processing:

- `data/nodeasset_trades.log`: raw normalized events from OpenClaw or direct ingestion.
- `data/nodeasset_openclaw_reasoned.log`: normalized events after reasoning.

## Commercial System Fit

This repo is an example customer-side integration for NodeAsset. It demonstrates:

- Recommended: NodeAsset API -> [`nodeasset-openclaw-trader`](https://github.com/nodeassetcorp/nodeasset-openclaw-trader) -> Market ML Databricks.
- Fallback: NodeAsset API -> Market ML Databricks direct endpoint.
- Legacy fallback: NodeAsset API -> local poller -> JSONL event log.

The recommended OpenClaw path lets the customer keep reasoning local. NodeAsset supplies subscribed specialist trades. [`nodeasset-openclaw-trader`](https://github.com/nodeassetcorp/nodeasset-openclaw-trader) receives and authenticates the NodeAsset side, OpenClaw gives the customer an agent surface for context, tools, market data, risk rules, portfolio state, compliance checks, and explanations, and Market ML Databricks persists and evaluates the resulting decisions.

This keeps NodeAsset's source of truth compact: trades remain global, subscriptions determine entitlement, and customer-side systems own downstream interpretation.

## Spark Note

This application does not currently use PySpark in the API, OpenClaw event path, direct poller, or reasoning layer. Spark dependencies are intentionally not installed in the local Docker runtime. If a future Databricks job needs Spark, add it to a separate Databricks job or job-specific image instead of the local API container.
