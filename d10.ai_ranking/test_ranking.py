import json
from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

agent = APIAnalysisAgent(api_key=GEMINI_API_KEY)
from utils import sample_endpoint

def test_rank_suggestions_by_importance():
    initial_response = agent.get_testing_suggestions_structured(sample_endpoint)
    suggestions_to_rank = initial_response.get("suggestions", [])

    assert len(suggestions_to_rank) >= 3, "Need at least 3 suggestions to rank."
    print(f"Original suggestions: {suggestions_to_rank}")

    # Define our most critical concepts from the Golden Dataset.
    golden_concepts = ["non-existent id", "invalid id"]

    # Ask the agent to rank the suggestions.
    ranked_response = agent.rank_testing_suggestions(suggestions_to_rank, golden_concepts)
    ranked_suggestions = ranked_response.get("ranked_suggestions", [])
    print(f"Ranked suggestions: {json.dumps(ranked_suggestions, indent=2)}")

    assert ranked_suggestions, "Ranking should not be empty."

    # Find the rank (index) of various test types.
    critical_case_rank = -1
    valid_case_rank = -1
    invalid_case_rank = -1

    for i, suggestion in enumerate(ranked_suggestions):
        s_lower = suggestion.lower()
        if ("non-existent" in s_lower or "not found" in s_lower) and critical_case_rank == -1:
            critical_case_rank = i
        if ("valid" in s_lower) and valid_case_rank == -1:
            valid_case_rank = i
        if ("invalid" in s_lower or "incorrect" in s_lower) and invalid_case_rank == -1:
            invalid_case_rank = i

    print(f"Rank of critical 'non-existent' case: {critical_case_rank}")
    print(f"Rank of first 'valid' case: {valid_case_rank}")
    print(f"Rank of first 'invalid' case: {invalid_case_rank}")

    # Critical case should be in the top half of the list.
    assert critical_case_rank != -1, "A critical case for non-existent IDs must be present."
    assert critical_case_rank < len(ranked_suggestions) / 2, \
        "The critical 'non-existent ID' test should be ranked in the top half of importance."

    # Valid cases are prioritized over invalid cases.
    if valid_case_rank != -1 and invalid_case_rank != -1:
        assert valid_case_rank < invalid_case_rank, \
            "Valid  cases should be ranked higher than invalid cases."
