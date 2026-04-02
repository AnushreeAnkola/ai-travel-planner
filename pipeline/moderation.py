from utils.llm_client import get_completion
import json

def moderate_inputs(destination, dates, budget, interests):
    delimiter = "####"
    user_message = f"""{delimiter}
    Destination: {destination}
    Dates: {dates}
    Budget: ${budget}
    Interests: {interests}
    {delimiter}"""

    model = "claude-sonnet-4-6"
    system_prompt = f"""
        You input moderator. You will be provided with a trip details delimited with {delimiter} characters.
        
        Your task is to check each query for the following things:
            - Is the destination a real place?
            - Are the dates valid and in the future?
            - Is the budget reasonable for the destination?
            - Are there any inappropriate or nonsensical inputs?
            - Flag if the budget seems too low for the destination and duration

        Respond with ONLY a JSON object, no markdown, no extra text:
        {{"is_valid": true or false, "errors": [list the errors you see with the input]}}
    """
    response = get_completion(user_message, system_prompt, model)
    print("RAW RESPONSE:", repr(response))  
    return json.loads(response)
