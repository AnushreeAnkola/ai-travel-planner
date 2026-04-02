from utils.llm_client import get_completion
import json

def plan_itinerary(destination, trip_type, num_days, interests, research):
    delimiter = "####"
    user_message = f"""{delimiter}
    Destination: {destination}
    Trip Type: {trip_type}
    Number of Days: {num_days}
    Interests: {interests}
    Research: {research}
    {delimiter}"""

    system_prompt = f"""
        You are a travel planner. You will be provided with trip details delimited with {delimiter} characters.
        
        Create a detailed day-by-day itinerary based on the research provided.
        For each day generate morning, afternoon and evening activities.

        Respond with ONLY a JSON object, do not wrap in markdown, no extra text:
        Do NOT use ```json or any markdown formatting.
        Start your response directly with {{ and end with }}.
        {{"days": [ 
            {{
                "day": 1,
                "morning": {{"activity": "...", "time": "9:00 AM", "description": "...", "reasoning": "..."}},
                "afternoon": {{"activity": "...", "time": "2:00 PM", "description": "...", "reasoning": "..."}},
                "evening": {{"activity": "...", "time": "7:00 PM", "description": "...", "reasoning": "..."}},
                "travel_time": "..."
            }}
        ]}}
    """
    response = get_completion(user_message, system_prompt, "claude-sonnet-4-5")
    print("RAW RESPONSE:", repr(response))
    return json.loads(response)