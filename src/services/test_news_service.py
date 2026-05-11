from src.services.news.news_service import (
    NewsService
)

service = NewsService()

news = service.get_news(
    "AAPL"
)

print("\n--- NEWS ---\n")

for article in news.data["news"]:

    print(
        f"Headline: "
        f"{article.headline}"
    )

    print(
        f"Summary: "
        f"{article.summary}"
    )

    print(
        f"Symbols: "
        f"{article.symbols}"
    )

    print(
        f"Source: "
        f"{article.source}"
    )

    print("---")