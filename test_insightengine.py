import pytest
from unittest.mock import patch
from app import search_web, generate_report  

# ----- Test search_web -----
@patch("app.DDGS")
def test_search_web(mock_ddgs):
    mock_instance = mock_ddgs.return_value.__enter__.return_value
    mock_instance.text.return_value = [{"body": "Result 1"}, {"body": "Result 2"}]

    result = search_web("AI trends", num_results=2)
    assert "Result 1" in result
    assert "Result 2" in result

# ----- Test generate_report with valid JSON -----
def test_generate_report_success(monkeypatch):
    class MockResponse:
        choices = [type("obj", (object,), {"message": type("msg", (object,), {"content": '{"summary":"Test","key_stats":[{"label":"Market Size","value":"100"} , {"label":"Growth Rate","value":"10%"}],"sentiment":"Positive"}'})()})]

    class MockClient:
        class chat:
            class completions:
                @staticmethod
                def create(**kwargs):
                    return MockResponse()

    monkeypatch.setattr("app.client", MockClient())  
    data = generate_report("AI Market", "dummy search data")
    assert "summary" in data
    assert "key_stats" in data
    assert len(data["key_stats"]) >= 2
    assert "sentiment" in data

def test_generate_report_fallback(monkeypatch):
    class MockClient:
        class chat:
            class completions:
                @staticmethod
                def create(**kwargs):
                    raise Exception("API fail")

    monkeypatch.setattr("app.client", MockClient())  
    data = generate_report("AI Market", "dummy search data")
    assert data["sentiment"] == "Neutral"
    assert "No active model" in data["key_stats"][0]["value"]
