from fastapi import APIRouter
from groq import Groq
from voyageai import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
  api_key=os.getenv("GROQ_API_KEY"),
)

embeddings_client = Client(
  api_key = os.getenv("VOYAGE_API_KEY")
)

router = APIRouter(prefix="/process", tags=["process"])


@router.post("/summary")
def get_summary(content:str):
  chat_completion = client.chat.completions.create(
    messages=[
      {
        "role": "user",
        "content": f"Summarize the text in 2-3 sentences. Be precise, no introduction needed: {content}",
      }
    ],
    model="llama3-70b-8192",
  )
  return chat_completion.choices[0].message.content

@router.post("/keywords")
def get_keywords(summary:str):
  chat_completion = client.chat.completions.create(
    messages=[
      {
        "role": "user",
        "content": 
          f""" 
            Generate 3-5 relevant keywords for an article's general topic. What areas of interest does the article cover?
            Avoid repetition, and keep the keywords general. Use plural case if necessary.
            This is the article's summary: {summary}.
            Answer ONLY with the keywords. Every keyword should be 1-2 words only. 
            Answer with a list of strings. Example format: ['keyword', 'keyword', 'keyword']
          """,
      }
    ],
    model="llama3-70b-8192",
  )
  return chat_completion.choices[0].message.content

@router.post("/embedding")
def get_embedding(text:str, client=embeddings_client):
  result = client.embed(text, model="voyage-2")
  return result.embeddings[0]

