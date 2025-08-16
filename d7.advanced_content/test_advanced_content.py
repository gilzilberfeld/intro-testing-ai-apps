import json
import re
from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
from utils import sample_endpoint

def test_advanced_content_validation():
    response_json = agent.get_testing_suggestions_structured(sample_endpoint)

    suggestions = response_json["suggestions"]
    all_suggestions_text = " ".join(suggestions).lower()

    # For a GET request, suggestions should use words related to checking or retrieving.
    expected_verbs = ["verify", "check", "get", "retrieve", "validate"]
    verb_found = any(verb in all_suggestions_text for verb in expected_verbs)
    assert verb_found, f"Suggestions should contain action verbs like {expected_verbs}"

    # The suggestions should mention testing the {id} path parameter
    # or common variations like "identifier".
    path_params = re.findall(r'\{(\w+)\}', sample_endpoint["path"])
    param_found = any(param in all_suggestions_text for param in path_params)
    assert param_found, f"Suggestions should mention the path parameter: {path_params[0]}"

    # Unrelated keyword check
    unrelated_keywords = ["payment", "product", "order"]
    unrelated_found = any(keyword in all_suggestions_text for keyword in unrelated_keywords)
    assert not unrelated_found, f"Suggestions contain unrelated keywords: {unrelated_keywords}"
