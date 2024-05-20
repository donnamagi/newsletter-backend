from bs4 import BeautifulSoup
import re

def remove_chars(text):
  """Remove extra spaces, newlines, and any script elements."""

  text = re.sub('\s+', ' ', text)
  text = re.sub('\n', ' ', text)
  text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)

  return text.strip()


def get_description(soup: BeautifulSoup):
  """Extract the meta description or og:description from the HTML."""

  description = ''
  meta_description = soup.find('meta', attrs={'name': 'description'})
  og_description = soup.find('meta', attrs={'property': 'og:description'})
  if meta_description:
    description = meta_description.get('content', '')
  elif og_description:
    description = og_description.get('content', '')

  return description


def get_body(soup: BeautifulSoup):
  """Extract the main body of text from the HTML."""

  paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
  paragraph_text = ' '.join(paragraphs)
  return paragraph_text[:3000]

def clean_text(soup: BeautifulSoup):
  """Main return function to clean the text."""
    
  description = get_description(soup)
  body = get_body(soup)
  summary = description + remove_chars(body)
  
  return summary
