import json
from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
from utils import sample_endpoint

def test_more_diversity():
    response_json = agent.get_testing_suggestions_structured(sample_endpoint)
    print(f"AI returned JSON: {json.dumps(response_json, indent=2)}")

    suggestions = response_json["suggestions"]
    all_suggestions_text = " ".join(s.lower() for s in suggestions)

    # Different test categories
    valid_keywords = ["valid", "correct", "existing"]
    invalid_keywords = ["invalid", "non-existent", "incorrect", "not found", "unauthorized"]
    special_keywords = ["empty", "no todos", "large number", "special characters"]

    # Check if at least one suggestion exists for each category
    has_valid_cases = any(keyword in all_suggestions_text for keyword in valid_keywords)
    has_invalid_cases = any(keyword in all_suggestions_text for keyword in invalid_keywords)
    has_special_cases = any(keyword in all_suggestions_text for keyword in special_keywords)

    print(f"Valid cases found: {has_valid_cases}")
    print(f"Invalid cases found: {has_invalid_cases}")
    print(f"Special cases found: {has_special_cases}")

    # Cover at least two different types of cases for a reasonably comprehensive test suite.
    assert (has_valid_cases + has_invalid_cases + has_special_cases) >= 2, \
        "The suggestions should cover at least two of: valid, invalid, or special."
