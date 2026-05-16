from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from chatbot import get_response

app = FastAPI()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root API

@app.get("/")
def home():
    return {
        "message": "Sri Lanka Railway Chatbot API"
    }

# Request model

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

# Chat API

@app.post("/chat")
def chat(request: ChatRequest):

    response = get_response(request.message, user_id=request.user_id)

    return {
        "response": response
    }