from src.services.news.news_classifier import (
    NewsClassifier
)

classifier = NewsClassifier()

headline = (
    "Apple surges after strong AI growth and bullish guidance"
)

result = classifier.classify(
    headline
)

print("\n--- CLASSIFICATION ---\n")

print(result)