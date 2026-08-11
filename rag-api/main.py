from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import ask_rag

# Initialize the FastAPI application
app = FastAPI(title="Portfolio RAG API")

# Define the expected JSON body for the POST request
class ChatRequest(BaseModel):
    question: str

# Define the expected JSON response
class ChatResponse(BaseModel):
    answer: str

# GET /health for uptime monitoring
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "rag-api"}

# POST /chat to handle incoming questions
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # Call the function you defined in rag.py
        answer = ask_rag(request.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        # Return a clean 500 error if the LangChain pipeline fails
        raise HTTPException(status_code=500, detail=str(e))