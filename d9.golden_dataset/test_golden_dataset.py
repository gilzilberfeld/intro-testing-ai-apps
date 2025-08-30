from unittest.mock import patch
from APIAnalysisAgent import APIAnalysisAgent

def test_suggestions_meet_golden_dataset_benchmark():
    golden_suggestions_concepts = [
        "valid user id",        # Happy path
        "non-existent id",      # Sad path
        "invalid id",           # Shocked path
        "user with no todos"    # Happy user
    ]

    agent = APIAnalysisAgent(api_key="fake_key")
    mock_ai_response = {
        "suggestions": [
            "Verify API returns a list of todos for a valid user ID.",
            "Test the response for a user that has an empty todo list.",
            "Check for a 404 error when using a user ID that does not exist.",
            "Attempt to retrieve todos with an incorrectly formatted ID (e.g., a string)."
        ]
    }

    with patch.object(agent, 'get_testing_suggestions_structured',
                      return_value=mock_ai_response):
        response_json = agent.get_testing_suggestions_structured(endpoint_info={})

    suggestions = response_json["suggestions"]
    all_suggestions_text = " ".join(s.lower() for s in suggestions)

    missing_concepts = []
    for concept in golden_suggestions_concepts:
        if concept not in all_suggestions_text:
            missing_concepts.append(concept)

    assert not missing_concepts, \
        f"The AI response is missing key concepts from the Golden Dataset: {missing_concepts}"

    # TODO: Add a real call and check against the golden dataset