# Market ML Databricks

Market ML Databricks is a customer-side listener and processing scaffold for the NodeAsset trade subscription system. It can connect directly to the NodeAsset API, or it can receive NodeAsset trade events from an OpenClaw agent. In both modes, it records each received trade as an event that downstream ML, analytics, execution, or alerting workflows can consume.

The repo also contains an earlier local ML pipeline for market data ingestion and model training. That pipeline is still useful as a scaffold, but the production integration points for NodeAsset are the direct `poller` service and the OpenClaw-compatible event ingestion API.

## What Users Will See

When a subscribed specialist starts producing trades on the next trading day, customers running this service will see the poller emit one summary line per polling cycle and write one JSON event per trade to the event log.

If no subscribed trades are available yet:

```json
{"timestamp":"2026-05-10T00:42:10.088055+00:00","status":"ok","count":0,"next_cursor":null}
```

When subscribed trades are available:

```json
{"timestamp":"2026-05-11T14:35:05.124000+00:00","status":"ok","count":2,"next_cursor":"184928"}
```

The event log receives one JSON line per trade:

```json
{"processed_at":"2026-05-11T14:35:05.120000+00:00","cursor":"184927","trade_id":"trd_01","specialist":"runner","symbol":"AAPL","side":"BUY","quantity":10,"price":184.22,"timestamp":"2026-05-11T14:34:59.000Z"}
{"processed_at":"2026-05-11T14:35:05.123000+00:00","cursor":"184928","trade_id":"trd_02","specialist":"ignition","symbol":"NVDA","side":"SELL","quantity":3,"price":921.15,"timestamp":"2026-05-11T14:35:01.000Z"}
```

Customers only receive trades for specialists they are subscribed to in NodeAsset. The filtering is enforced by the NodeAsset API using the authenticated user's email and subscription windows.

## System Context

This repo is one part of the larger NodeAsset commercial system:

```text
NodeAsset Terminal
  Customer selects active specialists: runner, ignition
        |
        v
NodeAsset API
  Stores subscriptions by user email and specialist
  Projects generated trades into subscribed user windows
  Exposes /gappers/subscribed-trades for authenticated customers
        |
        v
Market ML Databricks
  Option A: logs into NodeAsset and polls subscribed trades with a cursor
  Option B: receives NodeAsset trade events from an OpenClaw agent
  Writes normalized JSON events in both modes
        |
        v
Customer processing
  ML features, alerts, dashboards, execution reviews, reporting
```

The key design choice is that trades remain global in NodeAsset. Customer visibility is derived from subscriptions, not by duplicating separate trade streams for every user. That keeps the source of truth compact while still giving each customer a private feed. OpenClaw can sit between NodeAsset and this repo when the customer wants an agent runtime to own policy, routing, and automation decisions.

## Active Services

### Poller

The poller is the direct NodeAsset integration service.

Source: `src/services/poller.py`

Responsibilities:

- Login to the NodeAsset API with customer credentials.
- Call `GET /gappers/subscribed-trades`.
- Send the last processed cursor with `after_id`.
- Retry login when the token expires or is rejected.
- Persist the next cursor locally.
- Append each subscribed trade to a JSON-lines event log.
- Print a compact operational summary for container logs.

### OpenClaw Event Ingestion

The API can receive NodeAsset trade events from an OpenClaw agent. This mode is useful when the customer wants OpenClaw to manage NodeAsset authentication, specialist subscription handling, automation policy, and event routing.

Endpoints:

- `POST /events/nodeasset-trade`
- `POST /events/openclaw/nodeasset-trade`

Both endpoints accept either a raw NodeAsset trade object or an OpenClaw-style envelope:

```json
{
  "type": "nodeasset.trade.received",
  "data": {
    "cursor": "184927",
    "trade_id": "trd_01",
    "specialist": "runner",
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 10,
    "price": 184.22,
    "timestamp": "2026-05-11T14:34:59.000Z"
  }
}
```

The event is normalized and appended to the same `nodeasset_trades.log` file used by the direct poller.

### API

The FastAPI service exposes a small protected endpoint that can trigger the local ML pipeline.

Source: `src/api/main.py`

Endpoints:

- `GET /` returns service health.
- `POST /run` starts the local pipeline in the background.

In `TEST_MODE=true`, the API accepts a test JWT signed with `JWT_SECRET`. Outside test mode, it validates Azure JWTs using `AZURE_TENANT_ID` and `AZURE_AUDIENCE`.

### Local ML Pipeline

The legacy pipeline is organized as a simple medallion flow:

```text
src/ingestion/market_data.py
  yfinance -> data/raw/{SYMBOL}/{DATE}.csv

src/features/bronze.py
  raw CSVs -> data/bronze/market_data.parquet

src/features/silver.py
  cleaned parquet -> data/silver/market_data_clean.parquet

src/features/gold.py
  features and target -> data/gold/market_features.parquet

src/models/train.py
  RandomForestClassifier evaluation
```

This pipeline currently uses pandas, pyarrow, yfinance, and scikit-learn. It does not use PySpark.

## NodeAsset Feed Contract

The poller expects the NodeAsset API to provide:

```http
POST /user/login
Content-Type: application/json

{
  "email": "customer@example.com",
  "password": "..."
}
```

The login response must include one of:

- `token`
- `jwt`
- `access_token`
- `user.token`

The subscribed trade feed is called with the returned bearer token:

```http
GET /gappers/subscribed-trades?after_id=184928&limit=100
Authorization: Bearer <token>
```

Expected response shape:

```json
{
  "user_email": "customer@example.com",
  "count": 2,
  "next_cursor": "184930",
  "trades": [
    {
      "cursor": "184929",
      "trade_id": "trd_03",
      "specialist": "runner",
      "symbol": "AAPL",
      "side": "BUY",
      "quantity": 10,
      "price": 184.22,
      "timestamp": "2026-05-11T14:34:59.000Z"
    }
  ]
}
```

The poller treats the cursor as opaque. It stores the value returned by `next_cursor` and sends it as `after_id` on the next request.

## Configuration

The poller is configured entirely through environment variables.

| Variable | Default | Purpose |
| --- | --- | --- |
| `NODEASSET_API_URL` | `https://api.nodeasset.com` | Base URL for the NodeAsset API. |
| `NODEASSET_LOGIN_PATH` | `/user/login` | Login endpoint. |
| `NODEASSET_FEED_PATH` | `/gappers/subscribed-trades` | Subscribed trade feed endpoint. |
| `NODEASSET_EMAIL` | empty | NodeAsset customer email. Required at runtime. |
| `NODEASSET_PASSWORD` | empty | NodeAsset customer password. Required at runtime. |
| `NODEASSET_POLL_SECONDS` | `5` | Delay between feed polls. |
| `NODEASSET_LIMIT` | `100` | Maximum trades requested per poll. |
| `NODEASSET_ONCE` | `false` | Run one poll and exit. Useful for testing. |
| `NODEASSET_CURSOR_FILE` | `data/nodeasset_cursor.txt` | Cursor persistence file. |
| `NODEASSET_EVENT_LOG` | `data/nodeasset_trades.log` | JSON-lines trade event log. |
| `NODEASSET_HTTP_TIMEOUT` | `15` | HTTP timeout in seconds. |
| `EVENT_INGEST_TOKEN` | empty | Optional bearer or `X-Event-Token` value required by OpenClaw event ingestion endpoints. |

Never commit customer credentials. Pass them through the shell, CI secrets, or the deployment platform secret manager.

## Docker Usage

Build the poller image:

```sh
docker compose build poller
```

Run a one-shot smoke test:

```sh
NODEASSET_EMAIL='customer@example.com' \
NODEASSET_PASSWORD='...' \
NODEASSET_ONCE=true \
NODEASSET_LIMIT=10 \
docker compose run --rm poller
```

Run continuously:

```sh
NODEASSET_EMAIL='customer@example.com' \
NODEASSET_PASSWORD='...' \
NODEASSET_POLL_SECONDS=5 \
docker compose up poller
```

Run the API for OpenClaw event ingestion:

```sh
EVENT_INGEST_TOKEN='shared-secret' docker compose up api
```

Send a local OpenClaw-style event:

```sh
curl -X POST http://localhost:8000/events/openclaw/nodeasset-trade \
  -H 'Content-Type: application/json' \
  -H 'X-Event-Token: shared-secret' \
  -d '{
    "type": "nodeasset.trade.received",
    "data": {
      "trade_id": "trd_01",
      "specialist": "runner",
      "symbol": "AAPL",
      "side": "BUY",
      "quantity": 10,
      "price": 184.22,
      "timestamp": "2026-05-11T14:34:59.000Z"
    }
  }'
```

Stop services and remove the Compose network:

```sh
docker compose down
```

## Docker Images and Dependencies

The poller uses a dedicated lightweight dependency file:

```text
requirements-poller.txt
```

It intentionally installs only:

- `requests`
- `python-dotenv`

The broader `requirements.txt` supports the API and local ML pipeline. PySpark and py4j are intentionally not included because this application does not import Spark APIs or run Spark jobs.

## Data Files

The poller writes operational state under `data/` by default:

```text
data/nodeasset_cursor.txt
data/nodeasset_trades.log
```

`nodeasset_cursor.txt` lets the poller resume without replaying old trades.

`nodeasset_trades.log` is append-only JSON lines. It is the handoff point for downstream processors.

Example downstream reader:

```python
import json

with open("data/nodeasset_trades.log") as f:
    for line in f:
        trade = json.loads(line)
        print(trade["specialist"], trade["symbol"], trade["side"])
```

## Commercial Behavior

For a customer using the full NodeAsset product:

1. The customer logs into NodeAsset Terminal.
2. On Settings, the customer selects active specialists such as `runner` or `ignition`.
3. NodeAsset records the subscription by authenticated email.
4. When those specialists generate trades, NodeAsset projects visibility into that customer's subscription window.
5. Either this poller logs in as the same customer, or an OpenClaw agent logs in and forwards normalized trade events here.
6. The customer receives only subscribed trades.
7. The customer's local event log becomes the integration point for proprietary analysis, automation, dashboards, or ML workflows.

The customer should not see trades for unsubscribed specialists, expired subscription windows, other customers, or internal agent-only views.

## Direct Pull vs OpenClaw Push

Use direct pull when:

- The customer wants the simplest deployment.
- This repo is allowed to hold NodeAsset credentials.
- Cursor ownership belongs to this app.
- The output is mainly analytics or ML processing.

Use OpenClaw push when:

- The customer wants an agent runtime to mediate trade handling.
- NodeAsset credentials should live with the OpenClaw channel/plugin.
- The agent needs to reason, filter, annotate, alert, or route before the ML app stores the event.
- Multiple downstream consumers should receive the same NodeAsset event.

Both paths write the same normalized JSON-lines event format, so downstream processing does not need to care which integration mode produced the event.

## Deployment Notes

The repository includes Azure Container App infrastructure under `infra/envs/dev`. The existing GitHub workflow builds and deploys the poller container image to Azure Container Registry and updates the `poller-service` container app.

Before deploying for a real customer:

- Store `NODEASSET_EMAIL` and `NODEASSET_PASSWORD` as secrets.
- If using OpenClaw ingestion, store `EVENT_INGEST_TOKEN` as a shared secret and send it as `Authorization: Bearer <token>` or `X-Event-Token`.
- Confirm `NODEASSET_API_URL` points to the environment where `/gappers/subscribed-trades` is deployed.
- Mount or persist the cursor file if replay protection must survive container replacement.
- Ship `nodeasset_trades.log` to durable storage or replace the file writer with a queue/database sink.
- Monitor container logs for `status:error` messages.

## Local Verification Status

The current Docker poller path has been tested with Docker Compose:

```text
docker compose build poller
docker compose run --rm poller
```

The test completed successfully against the NodeAsset API and returned:

```json
{"status":"ok","count":0,"next_cursor":null}
```

That means the Docker execution environment is valid and the feed is reachable. A count of zero simply means no subscribed trades were available for that user at that cursor when the test ran.

## Repository Map

```text
docker-compose.yml              Compose services for api and poller
docker/Dockerfile.poller        Lightweight NodeAsset poller image
docker/Dockerfile.api           FastAPI image
requirements-poller.txt         Runtime deps for the poller
requirements.txt                API and local ML pipeline deps
src/services/poller.py          NodeAsset subscribed trade listener
src/services/trade_events.py    Shared event normalization and JSON-lines writer
src/api/main.py                 FastAPI health and pipeline trigger
src/ingestion/market_data.py    yfinance ingestion
src/features/bronze.py          Bronze parquet stage
src/features/silver.py          Silver cleaning stage
src/features/gold.py            Gold feature stage
src/models/train.py             Random forest model training
infra/envs/dev                  Azure infrastructure
```

## Roadmap

Recommended next product steps:

- Replace the local JSON-lines event log with a pluggable sink interface.
- Add sinks for Azure Event Hubs, Kafka, S3/ADLS, Postgres, or Databricks Delta.
- Add idempotency checks by `trade_id` in addition to cursor tracking.
- Add structured metrics for poll latency, received trade count, and API errors.
- Add a customer-facing sample dashboard fed by `nodeasset_trades.log`.
- Add integration tests using a mocked NodeAsset API response.
