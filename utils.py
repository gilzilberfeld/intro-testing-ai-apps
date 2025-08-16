sample_endpoint = {
    "method": "GET",
    "path": "/users/{id}/todos",
    "description": "Retrieves the to-do list for a specific user."
}


def print_suggestions(suggestions):
    print(f"AI returned {len(suggestions)} suggestions:")
    for i, s in enumerate(suggestions, 1):
        print(f"  {i}. {s}")
