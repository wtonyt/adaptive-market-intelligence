class NarrativeRegimeEngine:

    def detect_regime(
        self,
        narrative_summary
    ):

        if (
            narrative_summary.get(
                "AI_THEME",
                0
            ) >= 3
        ):

            return (
                "AI_BULLISH_REGIME"
            )

        elif (
            narrative_summary.get(
                "MACRO_EVENT",
                0
            ) >= 3
        ):

            return (
                "MACRO_RISK_REGIME"
            )

        elif (
            narrative_summary.get(
                "BEARISH_EVENT",
                0
            ) >= 3
        ):

            return (
                "BEARISH_NEWS_REGIME"
            )
        
        elif (
            narrative_summary.get(
                "LEADERSHIP_EVENT",
                0
            ) >= 2
        ):

            return (
                "LEADERSHIP_CONFIDENCE_REGIME"
            )

        elif (
            narrative_summary.get(
                "BUFFETT_THEME",
                0
            ) >= 1
        ):

            return (
                "VALUE_CONFIDENCE_REGIME"
            )

        return "NEUTRAL"