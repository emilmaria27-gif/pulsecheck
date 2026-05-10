# 📰 PulseCheck — AI News Sentiment Analyser

A live web application that fetches real news headlines, classifies them as positive or negative using a pre-trained AI model, and displays sentiment trends on an interactive dashboard.

 **Live demo:** [https://pulsecheck-3h3o.onrender.com](https://pulsecheck-3h3o.onrender.com)

---

## Features

- 🔍 Search any topic — technology, climate, sports, finance
- 🤖 AI sentiment classification using DistilBERT (HuggingFace)
- 📊 Interactive pie and bar charts powered by Plotly
- 📋 Full headlines table with confidence scores
- ⚡ Live data via NewsAPI

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Web Framework | Flask |
| AI / NLP | HuggingFace Transformers + DistilBERT |
| Data Processing | Pandas |
| Visualisation | Plotly |
| Data Source | NewsAPI |

---

## How to run locally

1. Clone the repository
git clone https://github.com/emilmaria27-gif/pulsecheck.git
cd pulsecheck

2. Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Create a `.env` file with your NewsAPI key
NEWS_API_KEY=your_newsapi_key_here

5. Run the app
python app.py

6. Visit `http://127.0.0.1:5000`

---

## How it works

1. User enters a search topic
2. Flask calls NewsAPI to fetch 50 real headlines
3. Each headline is passed through DistilBERT for sentiment classification
4. Results are organised into a pandas DataFrame
5. Plotly generates interactive charts from the data
6. Flask renders everything on the dashboard

---

Built by Emil Maria Sebastian
