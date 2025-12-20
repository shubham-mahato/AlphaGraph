import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from nlp_services.pipelines.news_event_pipeline import NewsEventPipeline
from data_ingestion.graph_writer.events_to_graph import EventGraphWriter
RAW_NEWS_DIR = Path("data_ingestion/raw/news")

def load_latest_news():
  files = sorted(RAW_NEWS_DIR.glob("*.json"))
  if not files:
    raise RuntimeError("No raw news files found in data_ingestion/raw/news")
  return files[-1]

def main():
  print("Starting AlphaGraph Ingestion Pipeline...")
  # 1. Load Data

  try:
    news_file = load_latest_news()
    print(f"Processing file: {news_file.name}")
    with open (news_file,"r",encoding="utf-8") as f:
      articles= json.load(f)
  except Exception as e:
    print(e)
    return
  
  # 2. NLP Processing
  pipelines = NewsEventPipeline()
  events = pipelines.process_articles(articles)
  print(f"NLP Pipeline extracted {len(events)} relevant financial events.")

  if not events:
    print("No event to write. Exiting...")
    return
  
  # 3. Write to graph

  writer = EventGraphWriter()
  writer.write_events(events)
  writer.close()

  print("SUCCESS: Events successfully written to Neo4j Graph!")

if __name__ == "__main__":
    main()
