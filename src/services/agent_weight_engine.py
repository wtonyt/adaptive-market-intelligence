from sqlalchemy import func

from src.db.database import SessionLocal
from src.db.models import AgentPerformance


def calculate_dynamic_weights():

    db = SessionLocal()

    try:

        agents = (
            db.query(
                AgentPerformance.agent_name
            )
            .distinct()
            .all()
        )

        if not agents:

            return {
                "ML": 0.5,
                "RL": 0.5
            }

        accuracy_scores = {}

        total_accuracy = 0

        for row in agents:

            agent_name = row[0]

            total = (
                db.query(AgentPerformance)
                .filter(
                    AgentPerformance.agent_name
                    == agent_name
                )
                .count()
            )

            correct = (
                db.query(AgentPerformance)
                .filter(
                    AgentPerformance.agent_name
                    == agent_name,

                    AgentPerformance.was_correct
                    == True
                )
                .count()
            )

            accuracy = (
                correct / total
            ) if total > 0 else 0

            accuracy_scores[
                agent_name
            ] = accuracy

            total_accuracy += accuracy

        # -----------------------------------
        # Normalize Weights
        # -----------------------------------

        if total_accuracy == 0:

            return {
                "ML": 0.5,
                "RL": 0.5
            }

        dynamic_weights = {}

        for agent_name, accuracy in (
            accuracy_scores.items()
        ):

            dynamic_weights[
                agent_name
            ] = (
                accuracy / total_accuracy
            )

        return dynamic_weights

    finally:

        db.close()


if __name__ == "__main__":

    weights = (
        calculate_dynamic_weights()
    )

    print(
        "\n===== DYNAMIC WEIGHTS =====\n",
        flush=True
    )

    print(weights)