# Services Reference

## Overview

The Market ML Platform is organized as a modular service-oriented architecture.

Each service has a focused responsibility and is designed to evolve independently as the platform scales.

---

# Poller Service

## Purpose

Consumes and generates trading signals.

## Responsibilities

- Signal ingestion
- Mock/live signal generation
- Service Bus publishing
- Event routing preparation

## Entry Point

```bash
python -m src.services.poller
Consensus Engine
Purpose

Combines ML and RL agent outputs into a unified decision.

Responsibilities
Adaptive weighting
Consensus scoring
Confidence modeling
Regime-aware decision making
Signal filtering
Entry Point
python -m src.services.consensus_engine
Market Regime Engine
Purpose

Classifies the current market environment.

Supported Regimes
Regime	Description
TRENDING	Directional market movement
VOLATILE	Elevated volatility
NEUTRAL	Balanced market conditions
Responsibilities
Market classification
Volatility analysis
Trend detection
Regime persistence logic
Entry Point
python -m src.services.market_regime_engine
Agent Weight Engine
Purpose

Dynamically adjusts influence between ML and RL agents.

Responsibilities
Performance-based weighting
Adaptive confidence scaling
Historical performance analysis
Agent ranking
Example Behavior
Stronger-performing agents receive more influence
Weak-performing agents are de-emphasized
Market regime can affect weighting logic
Position Sizing Engine
Purpose

Determines capital allocation per trade.

Inputs
Consensus confidence
Market regime
Portfolio exposure
Responsibilities
Adaptive sizing
Exposure scaling
Volatility-aware allocation
Risk normalization
Trade Management Engine
Purpose

Controls trade lifecycle decisions.

Responsibilities
Stop loss logic
Take profit logic
Max hold duration
Exit management
Trade state evaluation
Example Exit Types
Exit Type	Purpose
STOP_LOSS	Risk protection
TAKE_PROFIT	Profit realization
MAX_HOLD_TIME	Time-based risk control
Entry Point
python -m src.services.trade_management_engine
Portfolio Risk Engine
Purpose

Controls portfolio-level exposure and orchestration.

Responsibilities
Exposure throttling
Open position limits
Portfolio heat management
Aggregate risk management
Example Constraints
Max concurrent positions
Max deployed capital
Exposure thresholds
Entry Point
python -m src.services.portfolio_risk_engine
Portfolio State Engine
Purpose

Acts as the central portfolio ledger.

Responsibilities
Cash balance tracking
Open position tracking
Exposure calculation
Realized PnL tracking
Portfolio accounting
Managed State
State	Purpose
cash_balance	Available capital
open_positions	Active positions
realized_pnl	Closed trade performance
total_exposure	Current portfolio risk
Entry Point
python -m src.models.portfolio_state
Backtest Engine
Purpose

Simulates historical execution and portfolio behavior.

Responsibilities
Replay execution
Position lifecycle simulation
Capital accounting
Portfolio-aware execution
Managed trade exits
Performance tracking
Current Capabilities
Adaptive sizing
Regime-aware execution
Lifecycle management
Portfolio accounting
Planned Enhancements
Multi-symbol orchestration
Correlation awareness
Portfolio heat control
Distributed backtesting
Entry Point
python -m src.services.backtest_engine
Database Layer
Purpose

Provides persistent storage.

Current Database
PostgreSQL
Stored Data
Signal events
Consensus events
Market candles
Agent performance
Portfolio metrics
Service Bus Layer
Purpose

Provides event-driven communication.

Responsibilities
Message routing
Event distribution
Service decoupling
Future distributed scaling
Planned Evolution
Distributed workers
Async orchestration
Real-time signal routing
Multi-agent coordination
Long-Term Service Vision

The platform is evolving toward:

Distributed execution services
Real-time orchestration
Institutional portfolio management
Reinforcement learning coordination
Adaptive capital allocation
Multi-agent intelligence systems