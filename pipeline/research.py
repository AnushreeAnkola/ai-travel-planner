from utils.llm_client import get_completion
import json

def research_trip(destination, dates, interests, budget):
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
        
        You will need to follow the following steps to research the trip customer wants:

        Step 1: 
        {delimiter} First research 5 best areas/neighborhoods to stay. 

        Step 2:
        {delimiter} Then check online for weather expectations for the travel dates.

        Step 3:
        {delimiter} Check for local customs or tips.

        Step 4:
        {delimiter} Research and list 5 top must see attractions relevant to the trip
        based on their trip interest

        Step 5:
        {delimiter} Check for safety considerations

        Step 6:
        {delimiter} Check for local transportation options


        Respond with ONLY a JSON object, no markdown, no extra text:
        {{"neighborhoods": [...],
            "weather": "...",
            "customs": [...],
            "attractions": [...],
            "safety": "...",
            "transportation": [...]}}
    """
    response = get_completion(user_message, system_prompt, model)
    print("RAW RESPONSE:", repr(response))  
    return json.loads(response)

    