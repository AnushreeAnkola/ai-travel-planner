import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_completion(prompt, system="You are a helpful assistant.", temperature=1):
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text