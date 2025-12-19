import json
import requests
import sys
from datetime import datetime
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from config import NEWS_API_KEY, COMPANY_KEYWORDS

NEWS_API_URI = "https://newsapi.org/v2/everything"

RAW_NEWS_DIR = parent_dir / "raw" / "news"
RAW_NEWS_DIR.mkdir(parents=True, exist_ok=True)

def fetch_news(query:str):
  """
  Hits NewsAPI for a specific query.
  """

  params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10, 
        "apiKey": NEWS_API_KEY,
  }

  try:
    response =requests.get(NEWS_API_URI,params =params, timeout =10)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f" API Request failed for '{query}': {e}")
    return {"article": []}

def run_news_ingestion():
  print("Starting news ingestion....")
  all_articles=[]

  for keyword in COMPANY_KEYWORDS:
    print(f"Fetching news for: {keyword}")
    data = fetch_news(keyword)
    articles = data.get("articles",[])

    for art in articles:
      art["_query_keyword"] =keyword
    
    all_articles.extend(articles)

  if not all_articles:
    print("No article fetched. check your API key or internet.")
    return
  
  timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
  output_file = RAW_NEWS_DIR / f"news_{timestamp}.json"

  with open (output_file, "w", encoding="utf-8") as f:
    json.dump(all_articles, f, indent=2)
  
  print(f"Saved {len(all_articles)} articles to: {output_file}")

if __name__  == "__main__":
  run_news_ingestion()


