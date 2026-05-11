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

        # Macro narratives
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

        # AI / technology narratives
        elif any(keyword in headline_lower for keyword in [

            "ai",
            "artificial intelligence",
            "openai",
            "nvidia",
            "semiconductor",
            "machine learning"

        ]):

            event_type = "AI_THEME"

            sentiment = "BULLISH"

            confidence_adjustment = 0.03

        # Buffett / Berkshire narratives
        elif any(keyword in headline_lower for keyword in [

            "buffett",
            "berkshire"

        ]):

            event_type = "BUFFETT_THEME"

            sentiment = "LONG_TERM_BULLISH"

            confidence_adjustment = 0.02

        # Executive leadership
        elif any(keyword in headline_lower for keyword in [

            "ceo",
            "executive",
            "leadership",
            "tim cook",
            "satya nadella"

        ]):

            event_type = "LEADERSHIP_EVENT"

            sentiment = "NEUTRAL"

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