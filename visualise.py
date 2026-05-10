import requests
import pandas as pd
import plotly.express as px
from transformers import pipeline

API_KEY = "7ef7012f32b3474eaa3b3669fee0b107"
BASE_URL = "https://newsapi.org/v2/everything"

params = {
    "q": "technology",
    "language": "en",
    "pageSize": 50,
    "apiKey": API_KEY
}

# Fetch and analyse (same as before)
print("Fetching news...")
response = requests.get(BASE_URL, params=params)
data = response.json()
articles = data["articles"]

print("Loading AI model...")
sentiment_model = pipeline("sentiment-analysis")

print("Analysing headlines...")
results = []

for article in articles:
    title = article["title"]
    source = article["source"]["name"]
    published = article["publishedAt"][:10]

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

df = pd.DataFrame(results)

# --- CHART 1: Pie chart of sentiment breakdown ---
sentiment_counts = df["sentiment"].value_counts().reset_index()
sentiment_counts.columns = ["sentiment", "count"]

pie_chart = px.pie(
    sentiment_counts,
    names="sentiment",
    values="count",
    title="Overall Sentiment of Technology Headlines",
    color="sentiment",
    color_discrete_map={"POSITIVE": "#2ecc71", "NEGATIVE": "#e74c3c"}
)

pie_chart.write_html("pie_chart.html")
print("Pie chart saved!")

# --- CHART 2: Bar chart by news source ---
source_sentiment = df.groupby(["source", "sentiment"]).size().reset_index(name="count")

bar_chart = px.bar(
    source_sentiment,
    x="source",
    y="count",
    color="sentiment",
    title="Sentiment by News Source",
    color_discrete_map={"POSITIVE": "#2ecc71", "NEGATIVE": "#e74c3c"},
    barmode="group"
)

bar_chart.write_html("bar_chart.html")
print("Bar chart saved!")

print("\nDone! Open pie_chart.html and bar_chart.html in your browser.")