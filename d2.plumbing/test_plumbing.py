import pytest
from unittest.mock import patch
from google.api_core import exceptions
from APIAnalysisAgent import APIAnalysisAgent

@pytest.fixture
def agent():
    return APIAnalysisAgent(api_key="fake_key")

@pytest.fixture
def mock_endpoint_info():
    return {
        'method': '',
        'path': '',
        'description': ''
    }


def test_plumbing_generate_content_handles_garbage_response(agent, mock_endpoint_info):
    mock_response = "I'm sorry Dave, I'm afraid I can't do that."
    with patch.object(agent, '_call_model_api', return_value=mock_response):
        result = agent._generate_content(endpoint_info=mock_endpoint_info)
    assert result == []

def test_plumbing_handles_garbage_response(agent, mock_endpoint_info):
    mock_response = "I'm sorry Dave, I'm afraid I can't do that."
    with patch.object(agent, '_generate_content',
                      return_value=mock_response):
        suggestions = agent.get_testing_suggestions(endpoint_info=mock_endpoint_info)

    assert suggestions == []

def test_plumbing_handles_api_error_gracefully(agent, mock_endpoint_info):
    # Throw an error when trying to generate content
    with patch.object(agent, '_generate_content',
                      side_effect=exceptions.GoogleAPICallError("API is down")):
        suggestions = agent.get_testing_suggestions(endpoint_info=mock_endpoint_info)

    assert suggestions == []
