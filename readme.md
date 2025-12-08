# 🔍 The Insight Engine

The Insight Engine is a real-time research assistant that performs live web search and transforms the information into a structured dashboard using AI.  
Users simply enter a topic, and the system automatically:

1. Searches recent information on the web  
2. Analyzes the results using an AI model  
3. Returns a clean structured report including:
   - 📝 Executive summary  
   - 📊 Key statistics  
   - 🧭 Sentiment analysis  

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🔍 Real-time DuckDuckGo search | Fetches live web information |
| 🤖 AI-powered synthesis | Uses multiple fallback AI models |
| 🧱 Structured JSON output | Summary, stats & sentiment |
| 🛡️ Error-resistant | Handles malformed responses and rate limits |
| 🎨 Clean Streamlit UI | Simple and user-friendly |
| 🔁 Automatic model fallback | If one model is busy, another is used |

---

## 🧠 Tech Stack

- **Python 3.10+**
- **Streamlit** (Frontend)
- **DuckDuckGo Search API** (Real-time web scraping)
- **OpenRouter API** (LLM connection)
- **python-dotenv** (Secure API key handling)

---

## 📦 Installation

Clone this repository:

```sh
git clone https://github.com/Amurta1809/InsightEngine.git
cd InsightEngine
