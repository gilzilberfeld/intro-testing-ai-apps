import json
from APIAnalysisAgent import APIAnalysisAgent
from config import GEMINI_API_KEY

from utils import sample_endpoint
def test_flash_model_ranking_aligns_with_pro_model_benchmark():
    primary_agent = APIAnalysisAgent(api_key=GEMINI_API_KEY, model_name='gemini-1.5-flash-latest')
    #TODO Fix this
    judge_agent = APIAnalysisAgent(api_key=GEMINI_API_KEY, model_name='gemini-2.5-pro')

    golden_concepts = ["non-existent id", "invalid id"]

    initial_response = primary_agent.get_testing_suggestions_structured(sample_endpoint)
    suggestions_to_rank = initial_response.get("suggestions", [])
    assert len(suggestions_to_rank) >= 3, "Need at least 3 suggestions to rank."

    # Primary ranking
    primary_ranked_response = primary_agent.rank_testing_suggestions(suggestions_to_rank, golden_concepts)
    primary_ranking = primary_ranked_response.get("ranked_suggestions", [])

    # Benchmark ranking from our judge model
    judge_ranked_response = judge_agent.rank_testing_suggestions(suggestions_to_rank, golden_concepts)
    judge_ranking = judge_ranked_response.get("ranked_suggestions", [])

    print(f"\nPrimary Model Ranking:\n{json.dumps(primary_ranking, indent=2)}")
    print(f"\nJudge Model Ranking (our 'Truth'):\n{json.dumps(judge_ranking, indent=2)}")

    assert judge_ranking, "Judge model must provide a benchmark ranking."
    assert primary_ranking, "Primary model must provide a ranking to evaluate."

    # Primary ranking should align with the judge's.
    # Get the #1 most important suggestion according to the judge model.
    most_important_suggestion = judge_ranking[0]
    print(f"\nMost important suggestion (according to Pro): '{most_important_suggestion}'")

    # Find where our primary model ranked this most important suggestion.
    rank_in_primary_list = -1
    for i, suggestion in enumerate(primary_ranking):
        if suggestion == most_important_suggestion:
            rank_in_primary_list = i
            break

    print(f"Rank in primary agent list: {rank_in_primary_list}")

    # Primary model placed the most important item in its top 2 (resilient check).
    assert rank_in_primary_list != -1, "Primary ranking must contain the judge's top suggestion."
    assert rank_in_primary_list < 2, \
        ("The most important suggestion (as per the judge) should be "
         "in the top 2 of the primary model's ranking.")
