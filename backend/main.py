from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent
from ollama_client import ask_ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    user_email: str = ""

@app.get("/")
def home():
    return {
        "message": "AI Support Agent backend running"
    }

from ollama_client import ask_ollama


@app.post("/ask")
def ask(req: AskRequest):

    tool_result = run_agent(req.question)

    if tool_result:

        prompt = f"""
        User Question:
        {req.question}

        Tool Result:
        {tool_result}

        Explain this in a clear business-friendly way.
        """

        answer = ask_ollama(prompt)

        return {
            "answer": answer
        }

    answer = ask_ollama(req.question)

    return {
        "answer": answer
    }