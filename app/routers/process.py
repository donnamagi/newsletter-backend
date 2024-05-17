from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


client = Groq(
  api_key=os.getenv("GROQ_API_KEY"),
)

router = APIRouter(prefix="/llama", tags=["llama"])

class PromptRequest(BaseModel):
  prompt: str

@router.post("/chat")
def chat_to_llama(request : PromptRequest):
  chat_completion = client.chat.completions.create(
    messages=[
      {
        "role": "user",
        "content": request.prompt,
      }
    ],
    model="llama3-70b-8192",
  )
  return chat_completion.choices[0].message.content
