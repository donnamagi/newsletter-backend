import os
from dotenv import load_dotenv
from groq import AsyncGroq
from voyageai import Client
from bs4 import BeautifulSoup
from services.scrape import clean_text
import aiohttp

load_dotenv()

class ProcessService:
  def __init__(self):
    self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    self.embeddings_client = Client(api_key=os.getenv("VOYAGE_API_KEY"))

  async def get_content(self, url: str) -> str:
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        if response.status == 200:
          content = await response.text()
          soup = BeautifulSoup(content, 'html.parser')
          content = clean_text(soup)
          return content
        else:
          return None

  async def get_summary(self, content: str) -> str:
    chat_completion = await self.groq_client.chat.completions.create(
      messages=[
        {
          "role": "user",
          "content": f"Summarize the text in 2-3 sentences. Be precise, no introduction needed: {content}",
        }
      ],
      model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

  async def get_keywords(self, summary: str) -> str:
    chat_completion = await self.groq_client.chat.completions.create(
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

  async def get_embedding(self, summary: str) -> list:
    result = self.embeddings_client.embed(summary, model="voyage-2")
    return result.embeddings[0]

