from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
sample_endpoint = {
    "method": "GET",
    "path": "/users/{id}/todos",
    "description": "Retrieves the to-do list for a specific user."
}

def test_get_testing_suggestions_has_good_properties():
    suggestions = agent.get_testing_suggestions(sample_endpoint)

    print(f"AI returned {len(suggestions)} suggestions:")
    for i, s in enumerate(suggestions, 1):
        print(f"  {i}. {s}")

    # Check for a reasonable number of suggestions.
    assert 3 <= len(suggestions) <= 7, f"Expected 3-7 suggestions, but got {len(suggestions)}"

    # Check that each suggestion is a meaningful string.
    for suggestion in suggestions:
        assert isinstance(suggestion, str) and len(suggestion) > 10,\
            f"Suggestion '{suggestion}' is not a valid string."

