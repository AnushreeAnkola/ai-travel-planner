from utils.llm_client import get_completion
import json

def allocate_budget(destination, total_budget, num_days, itinerary, dining):
    delimiter = "####"
    user_message = f"""{delimiter}
    Destination: {destination}
    Total Budget: ${total_budget}
    Number of Days: {num_days}
    Itinerary: {itinerary}
    Dining: {dining}
    {delimiter}"""

    system_prompt = f"""
        You are a travel budget expert. You will be provided with trip details delimited with {delimiter} characters.
        
        Create a detailed budget breakdown for the trip.

        Respond with ONLY a JSON object, no markdown, no extra text:
        {{"accommodation_per_night": 0,
          "daily_food_budget": 0,
          "activity_costs_per_day": 0,
          "transportation": 0,
          "miscellaneous": 0,
          "total_estimated": 0,
          "user_budget": 0,
          "is_within_budget": true,
          "warnings": []
        }}
        Do NOT use ```json or any markdown formatting.
        Start your response directly with {{ and end with }}.
    """
    response = get_completion(user_message, system_prompt, "claude-sonnet-4-5")
    print("RAW RESPONSE:", repr(response))
    return json.loads(response)