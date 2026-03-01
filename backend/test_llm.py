from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLM_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-1.5-flash-latest",
    contents="Say hello in one sentence."
)

print(response.text)