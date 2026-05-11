from src.services.news.news_poller import (
    NewsPoller
)

poller = (
    NewsPoller()
)

poller.start()