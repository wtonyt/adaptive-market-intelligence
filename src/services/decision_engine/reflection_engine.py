import os

from openai import OpenAI

from src.db.database import SessionLocal

from src.db.models_decision import (
    DecisionRecord
)

from src.db.models_trade_outcome import (
    TradeOutcome
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ReflectionEngine:

    def reflect_on_trade(
        self,
        trade_id
    ):

        db = SessionLocal()

        try:

            decision = db.query(
                DecisionRecord
            ).filter(
                DecisionRecord.trade_id == trade_id
            ).first()

            outcome = db.query(
                TradeOutcome
            ).filter(
                TradeOutcome.trade_id == trade_id
            ).first()

            if not decision or not outcome:

                print(
                    "Missing decision or outcome"
                )

                return

            prompt = f"""
You are an institutional trading intelligence system.

Analyze this completed trade.

TRADE ID:
{decision.trade_id}

SYMBOL:
{decision.symbol}

DECISION DATA:
- Action: {decision.action}
- Confidence: {decision.confidence}
- Risk Score: {decision.risk_score}
- Approved: {decision.approved}

REASONS:
{decision.reasons}

BLOCKERS:
{decision.blockers}

OUTCOME:
- Entry Price: {outcome.entry_price}
- Exit Price: {outcome.exit_price}
- PnL: {outcome.pnl}
- Win: {outcome.win}
- Duration Minutes: {outcome.duration_minutes}

Provide:
1. Assessment of decision quality
2. Whether confidence was calibrated correctly
3. Key strengths in reasoning
4. Key weaknesses in reasoning
5. Suggestions for future improvements
"""

            response = client.chat.completions.create(

                model="gpt-5.1",

                messages=[
                    {
                        "role": "system",
                        "content":
                        "You are a financial intelligence reasoning engine."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            print("\n--- GPT REFLECTION ---\n")

            print(
                response.choices[0]
                .message.content
            )

        finally:

            db.close()