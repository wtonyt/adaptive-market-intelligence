# Market ML Platform

## Overview

Market ML Platform is an adaptive trading intelligence and portfolio orchestration system designed to simulate and eventually execute institutional-style trading workflows.

The platform combines:

- Signal ingestion
- Consensus intelligence
- Market regime detection
- Adaptive weighting
- Dynamic position sizing
- Trade lifecycle management
- Portfolio state tracking
- Performance feedback loops

The system is intentionally architected as a modular orchestration platform rather than a single trading script.

---

# Current Architecture

```text
Market Data
    ↓
Signal Generation
    ↓
Consensus Intelligence
    ↓
Market Regime Detection
    ↓
Adaptive Agent Weighting
    ↓
Position Sizing
    ↓
Trade Lifecycle Management
    ↓
Portfolio State Engine
    ↓
Performance Feedback
Core Components
Component	Purpose
Poller Service	Signal ingestion
Consensus Engine	Multi-agent decision logic
Market Regime Engine	Market environment classification
Position Sizing Engine	Adaptive capital allocation
Trade Management Engine	Stop loss / take profit / lifecycle logic
Portfolio State Engine	Exposure and portfolio accounting
Backtest Engine	Historical execution simulation
PostgreSQL	Persistent storage
Service Bus	Event distribution
Project Structure
market-ml-databricks/
│
├── src/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── api/
│
├── docs/
│   ├── architecture.md
│   ├── setup.md
│   ├── runbook.md
│   ├── services.md
│   └── trading-engine.md
│
├── docker-compose.yml
├── requirements.txt
└── README.md
Local Development Setup
Requirements
Python 3.9+
Docker Desktop
PostgreSQL
VS Code
Git
Environment Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Start PostgreSQL
docker compose up -d
Running the Platform
Run Consensus Engine
python -m src.services.consensus_engine
Run Backtest Engine
python -m src.services.backtest_engine
Run Market Regime Engine
python -m src.services.market_regime_engine
Backtesting Engine

The backtest engine simulates:

Signal-driven entries
Adaptive position sizing
Market regime awareness
Stop loss and take profit logic
Portfolio-aware capital accounting
Performance tracking

The engine is designed to evolve toward multi-position portfolio orchestration.

Portfolio Engine

PortfolioState acts as the central portfolio ledger.

Responsibilities include:

Tracking deployed capital
Tracking open positions
Exposure management
Realized PnL accounting
Portfolio-level orchestration
Current Features
Adaptive consensus engine
Dynamic agent weighting
Market regime detection
Adaptive position sizing
Trade lifecycle management
Portfolio state management
Performance persistence
Historical replay and backtesting
Planned Features
Multi-symbol orchestration
Live market execution
Alpaca integration
Correlation awareness
Sector exposure management
Drawdown protection
Portfolio heat management
Agent specialization
Reinforcement learning agents
Branching Strategy
Branch	Purpose
develop	Stable development branch
feature/*	Isolated feature development
main/master	Production-ready code

Examples:

feature/historical-market-data
feature/portfolio-risk-engine
feature/live-execution
Documentation
Document	Purpose
architecture.md	System architecture
setup.md	Local setup instructions
runbook.md	Operational procedures
services.md	Service reference
trading-engine.md	Trading intelligence design