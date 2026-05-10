from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

test_sentences = [
    "Apple launches revolutionary new product that changes everything",
    "Company faces massive data breach affecting millions of users",
    "Microsoft releases its quarterly earnings report today"
]

for sentence in test_sentences:
    result = sentiment_model(sentence)
    print(f"Text: {sentence}")
    print(f"Result: {result}")
    print("---")