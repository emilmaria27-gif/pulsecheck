from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
import requests
from textblob import TextBlob

load_dotenv()

app = Flask(__name__)

def analyse_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "POSITIVE", round(abs(analysis.sentiment.polarity) * 100, 2)
    else:
        return "NEGATIVE", round(abs(analysis.sentiment.polarity) * 100, 2)

def fetch_and_analyse(topic):
    API_KEY = os.getenv("NEWS_API_KEY")
    BASE_URL = "https://newsapi.org/v2/everything"

    params = {
        "q": topic,
        "language": "en",
        "pageSize": 50,
        "apiKey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    articles = data["articles"]

    results = []
    for article in articles:
        title = article["title"]
        source = article["source"]["name"]
        published = article["publishedAt"][:10]

        label, score = analyse_sentiment(title)

        results.append({
            "title": title,
            "source": source,
            "published": published,
            "sentiment": label,
            "confidence": score
        })

    return pd.DataFrame(results)

@app.route("/", methods=["GET", "POST"])
def index():
    topic = "technology"

    if request.method == "POST":
        topic = request.form.get("topic", "technology")

    df = fetch_and_analyse(topic)

    # Pie chart
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]
    pie = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        title=f"Sentiment Breakdown for '{topic}'",
        color="sentiment",
        color_discrete_map={"POSITIVE": "#2ecc71", "NEGATIVE": "#e74c3c"}
    )
    pie_html = pio.to_html(pie, full_html=False)

 # Bar chart
    source_sentiment = df.groupby(["source", "sentiment"]).size().reset_index(name="count")
    bar = px.bar(
        source_sentiment,
        x="source",
        y="count",
        color="sentiment",
        title=f"Sentiment by Source for '{topic}'",
        color_discrete_map={"POSITIVE": "#2ecc71", "NEGATIVE": "#e74c3c"},
        barmode="group"
    )
    bar_html = pio.to_html(bar, full_html=False)

    headlines = df[["title", "source", "published", "sentiment", "confidence"]].to_dict("records")

    return render_template("index.html",
        topic=topic,
        pie_html=pie_html,
        bar_html=bar_html,
        headlines=headlines
    )

if __name__ == "__main__":
    app.run(debug=True)
    