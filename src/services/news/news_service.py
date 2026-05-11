import os

from datetime import (
    datetime,
    timedelta
)

from dotenv import load_dotenv

from alpaca.data.historical.news import (
    NewsClient
)

from alpaca.data.requests import (
    NewsRequest
)

load_dotenv()


class NewsService:

    def __init__(self):

        self.client = NewsClient(

            api_key=os.getenv(
                "ALPACA_API_KEY"
            ),

            secret_key=os.getenv(
                "ALPACA_SECRET_KEY"
            )
        )

    def get_news(
        self,
        symbol
    ):

        request = NewsRequest(

            symbols=symbol,

            limit=5,

            start=(
                datetime.utcnow()
                - timedelta(days=2)
            )
        )

        news = self.client.get_news(
            request
        )

        return news