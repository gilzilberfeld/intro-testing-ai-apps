from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
sample_endpoint = {
    "method": "GET",
    "path": "/users/{id}/todos",
    "description": "Retrieves the to-do list for a specific user."
}

def test_get_testing_suggestions_returns_exactly_five_suggestions():
    suggestions = agent.get_testing_suggestions(sample_endpoint)
    assert len(suggestions) == 5

    print(f"AI returned {len(suggestions)} suggestions:")
    for i, s in enumerate(suggestions, 1):
        print(f"  {i}. {s}")

