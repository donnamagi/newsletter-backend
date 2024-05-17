from fastapi import APIRouter
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


client = Groq(
  api_key=os.getenv("GROQ_API_KEY"),
)

router = APIRouter(prefix="/llama", tags=["llama"])


@router.post("/get_summary")
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

@router.post("/get_keywords")
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
