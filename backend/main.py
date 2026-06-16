from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langgraph_agent import run_langgraph_agent


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
    user_email: str = "guest"


@app.get("/")
def home():
    return {
        "message": "AI WooCommerce Store Manager backend running with LangGraph"
    }


@app.post("/ask")
def ask(req: AskRequest):
    answer = run_langgraph_agent(
        question=req.question,
        user_email=req.user_email
    )

    return {
        "answer": answer
    }