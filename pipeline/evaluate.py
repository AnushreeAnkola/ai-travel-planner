from utils.llm_client import get_completion
import json

def evaluate_trip(user_dream_trip, reasoning, itinerary_plan, dining_suggestions, budget):
    system_prompt = f"""
        You are an assistant that evaluates how well the ai travel planner agent 
        answers a user question by looking at the context that ai travel planner 
        agent is using to generate its response.

        If issues are found, suggest specific fixes. 

        Respond with ONLY a JSON object, do not wrap in markdown, no extra text:
        Do NOT use ```json or any markdown formatting.
        Start your response directly with {{ and end with }}.


        Your task is to answer the following questions:
        - Is the assistant's response based only on the context provided (Y or N)
        - Does the answer include information that is not provided in context (Y or N)
        - Are activities mentioned in the itinerary plan geographically 
        logical (not zigzagging across the city)?
        - Is the pace reasonable (not 10 activities in one day)?
        - Does the budget add up?
        - Are there rest periods built in?
        - Does the itinerary match the original trip interest?
        - Overall quality score (1-10) with reasoning

        Respond with ONLY a JSON object, do not wrap in markdown, no extra text:
        Do NOT use ```json or any markdown formatting.
        Start your response directly with {{ and end with }}.
        {{
                "overall_score": 8,
                "checks": {{
                    "geographic_logic": {{"passed": true, "reasoning": "..."}},
                    "pace": {{"passed": false, "reasoning": "...", "suggestion": "..."}},
                    "budget_accuracy": {{"passed": true, "reasoning": "..."}},
                    "rest_periods": {{"passed": false, "reasoning": "...", "suggestion": "..."}},
                    "trip_type_match": {{"passed": true, "reasoning": "..."}}
                }},
                "overall_feedback": "...",
                "refinements": []
            }}
    """

    user_message = f"""
        You are evaluating a travel itinerary plan for a customer's travel 
        destination based on the user's dream trip details and their interests. 
        Here is the data:

        [BEGIN DATA]
        *************
        [User's Dream Trip] {user_dream_trip}
        *************
        [Context]:
        [Trip Interests] {reasoning}
        *************
        [Submissions:]
        [Itinerary Plan] {itinerary_plan}
        [Dining Suggestions] {dining_suggestions}
        [Budget] {budget}
        **************
        [END DATA]      
    """

    response = get_completion(user_message, system_prompt, "claude-sonnet-4-5")
    response = response.strip()
    if response.startswith("```"):
        response = response.split("```")[1]
        if response.startswith("json"):
            response = response[4:]
    response = response.strip()
    print("RAW RESPONSE:", repr(response))
    return json.loads(response)