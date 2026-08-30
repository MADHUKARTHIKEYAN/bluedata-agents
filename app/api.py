from fastapi import FastAPI
from pydantic import BaseModel

from app.graph.workflow import app_graph


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="BluAgents Marine Intelligence API",
    description="AI-powered marine and fishing assistance system",
    version="1.0.0",
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class AskRequest(BaseModel):
    question: str


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "BluAgents Marine Intelligence API",
    }


# --------------------------------------------------
# ASK ENDPOINT
# --------------------------------------------------

@app.post("/ask")
def ask(request: AskRequest):

    print(f"User question: {request.question}")

    result = app_graph.invoke(
        {
            "user_input": request.question
        }
    )

    return {
        "question": request.question,
        "intent": result.get("intent"),
        "response": result.get("response"),
    }
