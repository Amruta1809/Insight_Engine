import streamlit as st
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from openai import OpenAI
import json
import os

# Load environment variables
load_dotenv()

# Create OpenRouter Client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# System Prompt
SYSTEM_PROMPT = """
You are an AI research assistant. Based on the search results provided, generate structured insights.

Return ONLY valid JSON in this exact format:

{
  "summary": "A 2-paragraph executive-level summary.",
  "key_stats": [
    {"label": "Market Size", "value": "..."},
    {"label": "Growth Rate", "value": "..."}
  ],
  "sentiment": "Positive"
}

Rules:
- If the search results lack numerical data, infer reasonable placeholder values.
- ALWAYS include at least 2 objects in `key_stats`.
- Sentiment must be: Positive, Neutral, or Negative.
- DO NOT add commentary or markdown. Only return JSON.
"""


# Web Search 
def search_web(query, num_results=5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=num_results):
            results.append(r.get("body", ""))
    return "\n".join(results)


# AI Generation with Silent Fallback 
def generate_report(topic, search_data):

    models = [
        "meta-llama/llama-3.3-70b-instruct:free",
        "tngtech/deepseek-r1t2-chimera:free",
        "amazon/nova-2-lite-v1:free",
        "google/gemma-3-27b-it:free",
        "openai/gpt-oss-20b:free",
        "google/gemini-2.0-flash-exp:free"
    ]

    raw_response = None

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Topic: {topic}\n\nSearch Data:\n{search_data}"}
                ],
                extra_headers={
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "Insight Engine"
                }
            )
            raw_response = response.choices[0].message.content.strip()
            break  # Stop on success

        except Exception:
            continue  # Try next model silently

    # If all models fail
    if raw_response is None:
        return {
            "summary": "⚠️ All AI models are unavailable due to rate limits.",
            "key_stats": [
                {"label": "Status", "value": "No active model"},
                {"label": "Retry Suggestion", "value": "Try again later"}
            ],
            "sentiment": "Neutral"
        }

    # Cleanup formatting
    raw_response = raw_response.replace("```json", "").replace("```", "")

    # Safe JSON Parsing
    try:
        result = json.loads(raw_response)
    except:
        result = {
            "summary": "⚠️ Model did not return properly formatted JSON.",
            "key_stats": [
                {"label": "Formatting", "value": "Invalid JSON"},
                {"label": "Recovery Mode", "value": "Enabled"}
            ],
            "sentiment": "Neutral"
        }

    # Stats fallback if missing
    if not result.get("key_stats") or len(result["key_stats"]) < 2:
        result["key_stats"] = [
            {"label": "Data Availability", "value": "Limited"},
            {"label": "Extraction Confidence", "value": "Estimated"}
        ]

    return result


# UI 
st.set_page_config(page_title="Insight Engine", page_icon="🔍")

st.title("The Insight Engine")
topic = st.text_input("Enter a topic to research:")

if st.button("Generate Insights"):

    if topic.strip() == "":
        st.warning("Please enter a topic first.")
    else:
        st.write("Fetching data")
        web_results = search_web(topic)

        st.write("Analyzing information")
        data = generate_report(topic, web_results)

        # Display
        st.subheader("Summary:")
        st.write(data["summary"])

        st.subheader("Key Stats:")
        st.table(data["key_stats"])

        st.subheader("Sentiment:")
        sentiment_display = {
            "Positive": "🟢Positive",
            "Neutral": "⚪Neutral",
            "Negative": "🟠Negative"
        }
        st.write(sentiment_display.get(data["sentiment"], data["sentiment"]))
