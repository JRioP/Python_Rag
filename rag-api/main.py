import os
import secrets
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from rag import ask_rag

app = FastAPI(title="Portfolio RAG API")
API_KEY = os.getenv("API_KEY")  # if unset (local dev), the check is skipped


def verify_key(x_api_key: str | None = Header(default=None)):
    if API_KEY and not secrets.compare_digest(x_api_key or "", API_KEY):
        raise HTTPException(status_code=401, detail="Unauthorized")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "rag-api"}


@app.post("/chat", response_model=ChatResponse, dependencies=[Depends(verify_key)])
def chat(request: ChatRequest):
    try:
        return ChatResponse(answer=ask_rag(request.question))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))