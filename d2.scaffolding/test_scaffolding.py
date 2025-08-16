from unittest.mock import patch
from APIAnalysisAgent import APIAnalysisAgent

def test_suggestion_parser_scaffolding():
    # 1. SETUP: Create an agent and define a mock AI response.
    agent = APIAnalysisAgent(api_key="fake_key")
    mock_endpoint_info = {
        'method': '',
        'path': '',
        'description': ''
    }
    mock_ai_response_text = """
    1. First suggestion.
    2. Second suggestion.
    3. Third suggestion.
    """

    with patch.object(agent, '_generate_content', return_value=mock_ai_response_text):
        suggestions = agent.get_testing_suggestions(endpoint_info=mock_endpoint_info)

    assert len(suggestions) == 3
    assert suggestions[0] == "First suggestion."
    assert suggestions[1] == "Second suggestion."
    assert suggestions[2] == "Third suggestion."