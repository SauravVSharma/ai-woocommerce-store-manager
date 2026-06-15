import requests

def ask_ollama(question):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": question,
            "stream": False
        },
        timeout=120
    )

    return response.json()["response"]
