import requests
from fastapi import APIRouter
from bs4 import BeautifulSoup
from services.scrape import clean_text

router = APIRouter(tags=["scrape"])

@router.get("/scrape_content")
def scrape_content(url: str):
  content = requests.get(url)
  if content.status_code == 200:
    soup = BeautifulSoup(content.text, 'html.parser')

    summary = clean_text(soup)

    return summary
  else:
    return {"error": f"Error fetching content: {content.status_code}"}

