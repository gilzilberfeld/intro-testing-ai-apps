import pytest
from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY # Assuming your key is in a config file

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
sample_endpoint = {
    "method": "GET",
    "path": "/users/{id}/todos",
    "description": "Retrieves the to-do list for a specific user."
}

def test_get_testing_suggestions_returns_exactly_five_suggestions():
    """
    This test checks if the LLM adheres strictly to the prompt's instruction
    to generate exactly 5 test scenarios. It MAY or MAY NOT pass.
    """
    print("\n--- Running the Brittle Contract Test ---")

    # ACTION: Call the method to get suggestions from the live AI model.
    suggestions = agent.get_testing_suggestions(sample_endpoint)

    print(f"AI returned {len(suggestions)} suggestions:")
    for i, s in enumerate(suggestions, 1):
        print(f"  {i}. {s}")

    # ASSERTION: We assert that the length of the returned list is EXACTLY 5.
    # This is brittle because the AI might return 4, or 6, or format them differently.
    assert len(suggestions) == 5
