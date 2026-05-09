from collections import defaultdict

from sqlalchemy import func

from src.db.database import SessionLocal
from src.db.models import AgentPerformance


def generate_agent_metrics():
    db = SessionLocal()

    try:
        agents = (
            db.query(AgentPerformance.agent_name)
            .distinct()
            .all()
        )

        print("\n===== AGENT PERFORMANCE METRICS =====\n", flush=True)

        if not agents:
            print("No agent performance records found yet.", flush=True)
            return

        for agent_row in agents:
            agent_name = agent_row[0]

            total = (
                db.query(AgentPerformance)
                .filter(AgentPerformance.agent_name == agent_name)
                .count()
            )

            correct = (
                db.query(AgentPerformance)
                .filter(
                    AgentPerformance.agent_name == agent_name,
                    AgentPerformance.was_correct == True
                )
                .count()
            )

            avg_pnl = (
                db.query(func.avg(AgentPerformance.pnl))
                .filter(AgentPerformance.agent_name == agent_name)
                .scalar()
            )

            avg_confidence = (
                db.query(func.avg(AgentPerformance.confidence))
                .filter(AgentPerformance.agent_name == agent_name)
                .scalar()
            )

            accuracy = (correct / total) * 100 if total else 0

            print(f"Agent: {agent_name}", flush=True)
            print(f"  Total Signals: {total}", flush=True)
            print(f"  Accuracy: {round(accuracy, 2)}%", flush=True)
            print(f"  Avg Confidence: {round(avg_confidence or 0, 4)}", flush=True)
            print(f"  Avg PnL: {round(avg_pnl or 0, 4)}", flush=True)
            print("", flush=True)

    finally:
        db.close()


if __name__ == "__main__":
    generate_agent_metrics()