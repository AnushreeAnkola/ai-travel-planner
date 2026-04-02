from utils.llm_client import get_completion
import json

def suggest_dining(destination, trip_type, budget, itinerary):
    delimiter = "####"
    user_message = f"""{delimiter}
    Destination: {destination}
    Trip Type: {trip_type}
    Budget: ${budget}
    Itinerary: {itinerary}
    {delimiter}"""

    system_prompt = f"""
        You are a food and dining expert. You will be provided with trip details delimited with {delimiter} characters.
        
        Suggest dining options for each day of the itinerary.

        Respond with ONLY a JSON object, no extra text:
        {{"days": [
            {{
                "day": 1,
                "breakfast": {{"name": "...", "location": "...", "description": "...", "price_range": "..."}},
                "lunch": {{"name": "...", "location": "...", "description": "...", "price_range": "..."}},
                "dinner": {{"name": "...", "location": "...", "description": "...", "price_range": "..."}},
                "local_experience": "..."
            }}
        ]}}
        Do NOT use ```json or any markdown formatting.
        Start your response directly with {{ and end with }}.
    """
    response = get_completion(user_message, system_prompt, "claude-sonnet-4-5")
    print("RAW RESPONSE:", repr(response))
    return json.loads(response)