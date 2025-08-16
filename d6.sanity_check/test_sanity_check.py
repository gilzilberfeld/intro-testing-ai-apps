import json
from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
from utils import sample_endpoint

def test_structured_suggestions_have_relevant_content():
    response_json = agent.get_testing_suggestions_structured(sample_endpoint)
    print(f"AI returned JSON: {json.dumps(response_json, indent=2)}")

    assert "suggestions" in response_json and isinstance(response_json["suggestions"], list)
    suggestions = response_json["suggestions"]

    # Combine all suggestions into one lowercase string for easy searching.
    all_suggestions_text = " ".join(suggestions).lower()

    # Check for keywords related to the resource ("user, todo").
    assert "user" in all_suggestions_text, "Suggestions should mention the 'user' context"
    assert "todo" in all_suggestions_text, "Suggestions should be about 'todos'"

    # Check for common testing concepts (e.g., valid/invalid id).
    assert ("valid" in all_suggestions_text or
            "invalid" in all_suggestions_text or
            "non-existent" in all_suggestions_text), \
        "Suggestions should include common testing scenarios like valid/invalid IDs."
