from utils.llm_client import get_completion
import json

def classify_trip(destination, dates, interests, budget):
    delimiter = "####"
    user_message = f"""{delimiter}
    Destination: {destination}
    Dates: {dates}
    Budget: ${budget}
    Interests: {interests}
    {delimiter}"""

    model = "claude-sonnet-4-6"
    system_prompt = f"""
        You are a travel expert. You will be provided with a trip details delimited with {delimiter} characters.
        
        Your task is to classify each query into a one of the following category:
        Categories: adventure, relaxation, cultural, foodie, business, family, romantic, backpacker

        Respond with ONLY a JSON object, no markdown, no extra text:
        {{"trip_type": "category here", "reasoning": "one sentence explanation"}}
    """
    response = get_completion(user_message, system_prompt, model)
    print("RAW RESPONSE:", repr(response))  
    return json.loads(response)

    