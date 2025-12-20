import json
import sys
from pathlib import Path
from nlp_services.pipelines.news_event_pipeline import NewsEventPipeline

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))
RAW_NEWS_DIR = ROOT_DIR / "data_ingestion" / "raw" / "news"

def test_pipeline_smoke():
  files = list(RAW_NEWS_DIR.glob("*.json"))
  if not files:
    print("... SKIPPING TEST: No raw news files found ...")
    return
  
  latest_file = sorted(files)[-1]
  print(f"Testing with file: {latest_file.name}")

  with open (latest_file,"r",encoding="utf-8") as f:
    articles= json.load(f)
  
  pipeline = NewsEventPipeline()
  events = pipeline.process_articles(articles)
  assert len(events)>0, "Pipeline produced 0 events!"

  sample_event = events[0]
  print("\n SAMPLE EVENT OUTPUT:")
  print(sample_event.model_dump_json(indent=2))

  assert sample_event.event_id is not None
  assert isinstance(sample_event.sentiment, float)
  assert isinstance(sample_event.mentioned_entities, list)

  print("\n SMOKE TEST PASSED: Raw JSON -> Structured EventSchema works!")

if __name__ == "__main__":
    test_pipeline_smoke()