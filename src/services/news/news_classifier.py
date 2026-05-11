class NewsClassifier:

    def classify(
        self,
        headline
    ):

        headline_lower = (
            headline.lower()
        )

        event_type = "GENERAL"

        sentiment = "NEUTRAL"

        confidence_adjustment = 0.0

        risk_adjustment = 0.0

        # Bullish classifications
        if any(keyword in headline_lower for keyword in [

            "upgrade",
            "beats",
            "surges",
            "strong demand",
            "bullish",
            "record earnings",
            "growth",
            "raises guidance",
            "ai expansion"

        ]):

            event_type = "BULLISH_EVENT"

            sentiment = "BULLISH"

            confidence_adjustment = 0.05

        # Bearish classifications
        elif any(keyword in headline_lower for keyword in [

            "downgrade",
            "lawsuit",
            "investigation",
            "fraud",
            "declines",
            "weak guidance",
            "misses",
            "layoffs",
            "sec"

        ]):

            event_type = "BEARISH_EVENT"

            sentiment = "BEARISH"

            confidence_adjustment = -0.10

            risk_adjustment = 0.15

        # Macro risk
        elif any(keyword in headline_lower for keyword in [

            "inflation",
            "fed",
            "interest rates",
            "recession",
            "geopolitical"

        ]):

            event_type = "MACRO_EVENT"

            sentiment = "CAUTION"

            risk_adjustment = 0.10

        return {

            "event_type":
                event_type,

            "sentiment":
                sentiment,

            "confidence_adjustment":
                confidence_adjustment,

            "risk_adjustment":
                risk_adjustment
        }