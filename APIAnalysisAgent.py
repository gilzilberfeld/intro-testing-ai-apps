import google.generativeai as genai
from google.generativeai import types
from google.api_core import exceptions
import json


class APIAnalysisAgent:
    def __init__(self, api_key, model_name='gemini-1.5-flash-latest'):
        # In a real app, handle the case where the key is missing/invalid
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.config = types.GenerationConfig(max_output_tokens=400)

    def _generate_content(self, prompt_text, system_instruction):
        """A private helper method to handle AI content generation and errors."""
        try:
            model = genai.GenerativeModel(self.model_name, system_instruction=system_instruction)
            response = model.generate_content(prompt_text, generation_config=self.config)
            return response.text
        except (exceptions.GoogleAPICallError, exceptions.RetryError, ValueError) as e:
            print(f"An API error occurred with model {self.model_name}: {e}")
            return ""  # Return an empty string on failure

    def get_testing_suggestions(self, endpoint_info):
        """
        Generate specific testing suggestions for an endpoint.
        """
        prompt = f"""
        Generate 5 specific test scenarios for this API endpoint:

        Method: {endpoint_info['method']}
        Path: {endpoint_info['path']}
        Description: {endpoint_info['description']}

        For each test, provide just the test name in this format:
        1. Test name here
        2. Test name here
        etc.

        Focus on practical tests that would catch real issues.
        """
        system_instruction = "You are an expert API tester. Generate practical test scenarios."

        try:
            response_text = self._generate_content(prompt, system_instruction)
        except exceptions.GoogleAPICallError as e:
            print(f"An API error occurred while generating suggestions: {e}")
            return []

        if not response_text:
            return []

        # Parse response.text into list
        suggestions = []
        for line in response_text.split('\n'):
            if line.strip() and any(char.isdigit() for char in line[:5]):
                test_name = line.split('.', 1)[1].strip() if '.' in line else line.strip()
                suggestions.append(test_name)

        return suggestions[:5]

    def get_testing_suggestions_structured(self, endpoint_info):
        """
        Generate specific testing suggestions for an endpoint as a structured JSON object.
        """
        prompt = f"""
        Generate 5 specific test scenarios for this API endpoint:

        Method: {endpoint_info['method']}
        Path: {endpoint_info['path']}
        Description: {endpoint_info['description']}

        Return the response as a single, valid JSON object.
        The JSON object should have one key: "suggestions".
        The value for "suggestions" should be an array of strings, where each string is a test scenario name.

        Return ONLY the JSON object and nothing else.
        """
        system_instruction = "You are an expert API tester that only returns valid JSON."
        response_text = self._generate_content(prompt, system_instruction)

        if not response_text:
            return {"suggestions": []}

        try:
            clean_response = response_text.strip().replace('```json', '').replace('```', '').strip()
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {"suggestions": []}

    def rank_testing_suggestions(self, suggestions, golden_concepts):
        """
        Uses an AI Judge to rank a list of suggestions based on importance,
        guided by a set of golden concepts.
        """
        prompt = f"""
        You are an expert test analyst. Your task is to rank the following test suggestions based on their importance for ensuring API quality.

        Here are the most critical test concepts to prioritize:
        {', '.join(golden_concepts)}

        Here is the list of test suggestions to rank:
        {json.dumps(suggestions)}

        Return a single, valid JSON object with one key: "ranked_suggestions".
        The value should be an array of strings, with the most important suggestion first and the least important last.

        Return ONLY the JSON object.
        """
        system_instruction = "You are an expert test analyst that returns ranked lists in valid JSON."
        response_text = self._generate_content(prompt, system_instruction)

        if not response_text:
            return {"ranked_suggestions": []}

        try:
            clean_response = response_text.strip().replace('```json', '').replace('```', '').strip()
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {"ranked_suggestions": []}