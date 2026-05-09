# Operational Runbook

## Purpose

This document provides operational procedures for starting, running, validating, and troubleshooting the Market ML Platform.

The runbook is intended to support:

- Local development
- Service recovery
- Platform onboarding
- Troubleshooting
- Operational continuity

---

# Environment Requirements

## Required Software

Install the following:

- Python 3.9+
- Docker Desktop
- PostgreSQL
- Git
- VS Code

Optional future tooling:

- Terraform
- Azure CLI
- Databricks CLI

---

# Project Startup Procedure

## 1. Open Project

Navigate to the project root:

```bash
cd ~/projects/market-ml-databricks
2. Activate Python Environment
source .venv/bin/activate

Verify:

which python

Expected output should reference:

.venv/bin/python
3. Start Docker Desktop

Verify Docker Desktop is running before starting PostgreSQL.

4. Start PostgreSQL Container
docker compose up -d

Verify container status:

docker ps

Expected:

PostgreSQL container running
Healthy status
5. Validate Database Connectivity

Use:

pgAdmin
DBeaver
psql CLI

Verify:

Database accessible
Tables visible
Inserts functioning
Core Service Startup
Run Consensus Engine
python -m src.services.consensus_engine

Expected:

Consensus results generated
Regime detection output
Confidence scores displayed
Run Market Regime Engine
python -m src.services.market_regime_engine

Expected:

Regime classification
Volatility metrics
Trend analysis
Run Portfolio Risk Engine
python -m src.services.portfolio_risk_engine

Expected:

Exposure checks
Position limit validation
Run Trade Management Engine
python -m src.services.trade_management_engine

Expected:

Stop loss evaluation
Take profit evaluation
Lifecycle checks
Run Backtest Engine
python -m src.services.backtest_engine

Expected:

Position entries
Managed exits
Portfolio accounting
PnL reporting
Portfolio summary
Expected Backtest Lifecycle
Signal
    ↓
Consensus
    ↓
Regime Detection
    ↓
Position Sizing
    ↓
Portfolio Validation
    ↓
Trade Entry
    ↓
Lifecycle Management
    ↓
Managed Exit
    ↓
Performance Feedback
Health Checks
Docker Health

Verify:

docker ps

Ensure:

Containers are running
No restart loops
PostgreSQL healthy
Database Health

Verify:

Signal events exist
Consensus events persist
Candle data available
Performance records updating
Portfolio Validation

Verify:

Cash balance changes
Exposure updates
PnL tracking functions
Open positions tracked correctly
Common Issues
Docker Not Running
Symptoms
Cannot connect to Docker daemon
Resolution

Start Docker Desktop.

Then rerun:

docker compose up -d
PostgreSQL Connection Failure
Symptoms
Connection refused
Resolution

Verify:

docker ps

Ensure PostgreSQL container is active.

Python Import Errors
Symptoms
ModuleNotFoundError
Resolution

Always execute from project root using:

python -m module.path

Example:

python -m src.services.backtest_engine
Missing Consensus Events
Symptoms
No consensus output
No database inserts
Resolution

Verify:

Consensus engine running
Database active
Signal events present
Backtest Produces No Trades
Symptoms
Entries: 0
Closed Trades: 0
Resolution

Verify:

Consensus engine running
Signal events exist
Candle data exists
Position sizing not returning zero
Immediate Trade Exits
Symptoms

Trades exit immediately after entry.

Resolution

Verify:

continue exists after trade entry
Lifecycle management logic not nested incorrectly
bars_held increments correctly
Full Environment Restart
Shutdown
docker compose down
Restart
docker compose up -d

Restart services afterward.

Git Workflow
Start New Feature Branch
git checkout develop
git pull
git checkout -b feature/new-feature
Commit Changes
git add .
git commit -m "description"
git push
Merge Strategy
Complete feature branch
Validate locally
Merge into develop
Validate platform stability
Promote toward production branch
Operational Philosophy

The platform is evolving toward:

Adaptive Portfolio Intelligence Infrastructure

This means:

services become interconnected
portfolio state becomes central
execution becomes adaptive
intelligence becomes feedback-driven

Operational discipline becomes increasingly important as platform complexity grows.