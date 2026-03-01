import requests
import json


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"


def call_llm(prompt: str):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            raise Exception(response.text)

        data = response.json()
        return data["response"]

    except Exception as e:
        raise Exception(f"Ollama Error: {str(e)}")