from utils.llm_client import get_completion

response = get_completion("Say hello and confirm you're working.")
print(response)