from src.services.news.news_service import (
    NewsService
)

from src.services.news.news_classifier import (
    NewsClassifier
)


class NewsIntelligenceEngine:

    def __init__(self):

        self.news_service = (
            NewsService()
        )

        self.classifier = (
            NewsClassifier()
        )

    def evaluate(
        self,
        context
    ):

        sentiment_adjustment = 0.0

        risk_adjustment = 0.0

        news_factors = []

        try:

            news = (
                self.news_service.get_news(
                    context.symbol
                )
            )

            articles = (
                news.data.get(
                    "news",
                    []
                )
            )

            for article in articles[:3]:

                classification = (
                    self.classifier.classify(
                        article.headline
                    )
                )

                sentiment_adjustment += (
                    classification[
                        "confidence_adjustment"
                    ]
                )

                risk_adjustment += (
                    classification[
                        "risk_adjustment"
                    ]
                )

                news_factors.append(

                    f"{classification['event_type']}: "

                    f"{article.headline}"
                )

        except Exception as e:

            news_factors.append(
                f"News evaluation failed: {e}"
            )

        return {

            "sentiment_adjustment":
                round(
                    sentiment_adjustment,
                    2
                ),

            "risk_adjustment":
                round(
                    risk_adjustment,
                    2
                ),

            "news_factors":
                news_factors
        }