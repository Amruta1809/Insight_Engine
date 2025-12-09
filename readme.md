# The Insight Engine

The Insight Engine is a real-time research assistant that performs live web search and transforms the information into a structured dashboard using AI.  
Users simply enter a topic, and the system automatically:

1. Searches recent information on the web  
2. Analyzes the results using an AI model  
3. Returns a clean structured report including:
   -  Executive summary  
   -  Key statistics  
   -  Sentiment analysis  

---

## Features

-The Insight Engine is an AI-powered research assistant.

-The user enters a topic and the tool searches the internet automatically.

-The web results are processed by an AI model through OpenRouter API.

-The AI returns information in a structured JSON format (summary, stats, sentiment).

-The app is built using Streamlit for a clean and interactive UI.

-Key insights are shown in tables, text sections, and sentiment badges.

---

##  Tech Stack

- **Python 3.10+**
- **Streamlit** (Frontend)
- **DuckDuckGo Search API** (Real-time web scraping)
- **OpenRouter API** (LLM connection)
- **python-dotenv** (Secure API key handling)

---

## setup
 1.Install Required Libraries

    pip install -r requirements.txt
 2.Run the Application

    streamlit run app.py

---

##  Installation

Clone this repository:

```sh
git clone https://github.com/Amurta1809/InsightEngine.git
cd InsightEngine


