import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_completion(user_message, system_prompt, model):
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages = [
            {"role": "user", "content": user_message}
        ]
    )
    return message.content[0].text