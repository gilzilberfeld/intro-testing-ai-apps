import json
from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
from utils import sample_endpoint

def test_get_structured_suggestions_has_valid_schema():
    response_json = agent.get_testing_suggestions_structured(sample_endpoint)
    print(f"AI returned JSON: {json.dumps(response_json, indent=2)}")

    # --- SCHEMA VERIFICATION ---
    assert isinstance(response_json, dict), "Response should be a dictionary"
    assert "suggestions" in response_json, "JSON must contain the 'suggestions' key"

    suggestions = response_json["suggestions"]
    assert isinstance(suggestions, list), "The 'suggestions' key should contain a list"
    assert len(suggestions) > 0, "The suggestions list should not be empty"

    for item in suggestions:
        assert isinstance(item, str), f"Item '{item}' is not a string"