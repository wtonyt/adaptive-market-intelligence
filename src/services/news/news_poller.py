import time

from datetime import datetime

from src.schemas.intelligence_event import (
    IntelligenceEvent
)

from src.services.news.news_service import (
    NewsService
)

from src.services.intelligence_router import (
    IntelligenceRouter
)


class NewsPoller:

    def __init__(self):

        self.news_service = (
            NewsService()
        )

        self.router = (
            IntelligenceRouter()
        )

        self.seen_headlines = set()

    def start(
        self,
        symbol="AAPL"
    ):

        print(
            "\nStarting News Poller..."
        )

        while True:

            try:

                news = (
                    self.news_service.get_news(
                        symbol
                    )
                )

                articles = (
                    news.data.get(
                        "news",
                        []
                    )
                )

                for article in articles:

                    if (
                        article.headline
                        in self.seen_headlines
                    ):

                        continue

                    self.seen_headlines.add(
                        article.headline
                    )

                    event = IntelligenceEvent(

                        event_type="NEWS_EVENT",

                        symbol=symbol,

                        source="alpaca_news",

                        timestamp=datetime.utcnow(),

                        payload={
                            "symbol": symbol,
                            "headline": article.headline,
                            "summary": article.summary
                        }
                    )

                    self.router.route(
                        event
                    )

                time.sleep(30)

            except Exception as e:

                print(
                    f"\nNews Poller Error: {e}"
                )