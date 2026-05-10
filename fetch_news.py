import requests
import pandas as pd
from transformers import pipeline

API_KEY = "7ef7012f32b3474eaa3b3669fee0b107"
BASE_URL = "https://newsapi.org/v2/everything"

params = {
    "q": "technology",
    "language": "en",
    "pageSize": 50,
    "apiKey": API_KEY
}

print("Fetching news.....");
response  = requests.get(BASE_URL, params=params)
data = response.json()
articles = data["articles"]

# Load AI model
print("Loading AI model...")
sentiment_model = pipeline("sentiment-analysis")

# Analyse headlines and collect results
print("Analysing headlines...")
results = []

for article in articles:
    title = article["title"]
    source = article["source"]["name"]
    published = article["publishedAt"][:10]  # just the date, not time

    result = sentiment_model(title[:512])[0]
    label = result["label"]
    score = round(result["score"] * 100, 2)

    results.append({
        "title": title,
        "source": source,
        "published": published,
        "sentiment": label,
        "confidence": score
    })
    
# Build the DataFrame
df = pd.DataFrame(results)

# Explore the data
print("\n--- DATAFRAME PREVIEW ---")
print(df.head())

print("\n--- SENTIMENT COUNTS ---")
print(df["sentiment"].value_counts())

print("\n--- AVERAGE CONFIDENCE BY SENTIMENT ---")
print(df.groupby("sentiment")["confidence"].mean().round(2))
