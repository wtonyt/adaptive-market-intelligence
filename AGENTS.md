# Market ML Databricks — Agent Instructions

## Project Overview

Stock market ML pipeline using **Medallion Architecture** (raw → bronze → silver → gold).  
Predicts next-day market direction (binary classification) for AAPL, MSFT, NVDA, SPY.

## Architecture

```
src/ingestion/    → Fetch stock data from yfinance → data/raw/{SYMBOL}/{DATE}.csv
src/features/     → bronze.py → silver.py → gold.py  (each stage is independently runnable)
src/models/       → Train RandomForest on gold features
src/workflows/    → run_pipeline.py orchestrates all stages end-to-end
src/api/          → FastAPI: GET / (health), POST /run (triggers pipeline, requires X-API-Key header)
src/backtesting/  → Placeholder (empty)
src/llm/          → Placeholder (empty)
```

**Data layer files:**
- `data/bronze/market_data.parquet` — consolidated raw CSVs + symbol column
- `data/silver/market_data_clean.parquet` — cleaned, typed, sorted
- `data/gold/market_features.parquet` — ML features + binary `target` column

## Running the Pipeline

```bash
# Full pipeline (sequential)
python src/ingestion/market_data.py
python src/features/bronze.py
python src/features/silver.py
python src/features/gold.py
python src/models/train.py

# Or via orchestrator
python src/workflows/run_pipeline.py

# Start API server
uvicorn src.api.main:app --reload

# Trigger via API
curl -X POST http://localhost:8000/run -H "X-API-Key: supersecret123"
```

## Key Conventions

- Each feature module follows **load → transform → save** pattern; each is independently executable
- Use `pandas.DataFrame.copy()` when slicing to avoid `SettingWithCopyWarning`
- Drop NAs aggressively at each layer rather than imputing
- Gold layer adds: `return`, `ma_5`, `ma_10`, `volatility_5`, `next_return`, `target`
- Python **3.11**, dependencies in `requirements.txt`; `pyproject.toml` and `src/requirements.txt` are currently empty/duplicates
- API key loaded from `.env` (`API_KEY=supersecret123`) — never hardcode secrets

## Installed But Not Yet Integrated

- **MLflow** — experiment tracking (planned integration in `src/models/`)
- **PySpark / Databricks SDK** — distributed processing (planned migration target)
- **SQLAlchemy / Alembic** — database ORM (placeholder)
- **Flask** — not used (FastAPI is the chosen framework)

## Tests & Config

- `tests/` is empty — no test suite exists yet
- `config/`, `notebooks/`, `terraform/` are empty placeholders
- Docker entrypoint currently runs ingestion only (`docker/Dockerfile`)
