import hashlib
from typing import List
import json
from pathlib import Path
from nlp_services.schemas.event_schema import EventSchema
from nlp_services.models.ner_models import NERModel
from nlp_services.models.sentiment_model import SentimentModel
from nlp_services.mapping.entity_mapper import EntityMapper

class NewsEventPipeline:
  def __init__(self):
    self.ner = NERModel()
    self.sentiment = SentimentModel()

    current_file = Path(__file__).resolve()
    mapping_dir = current_file.parents[1] / "mapping"
    alias_path = mapping_dir / "company_aliases.json"

    if not alias_path.exists():
      raise FileNotFoundError(f"Critical: Alias map not found at {alias_path}") 
    
    with open(alias_path,"r", encoding="utf-8") as f:
      alias_map = json.load(f)
    
    self.entity_mapper = EntityMapper(alias_map)

  def classify_event_type(self,text:str) ->str:
    text = text.lower()

    if any(k in text for k in ["earnings", "profit", "revenue", "q1", "q2", "q3", "q4"]):
      return "earnings"
    if any(k in text for k in ["acquire", "merger", "buyout", "deal"]):
      return "m&a"
    if any(k in text for k in ["regulation", "rbi", "sebi", "government", "ban", "policy"]):
      return "regulation"
    if any(k in text for k in ["lawsuit", "court", "legal", "fraud", "scam"]):
      return "legal"
    return "general"
  
  def generate_event_id(self,title:str,timestamp:str)->str:
    base = f"{title}_{timestamp}"
    return hashlib.md5(base.encode()).hexdigest()
  
  def process_article(self,article:dict) ->EventSchema:
    title = article.get("title") or ""
    description = article.get("description") or ""
    content = article.get("content") or ""
    published_at = article.get("publishedAt")

    text_blob = f"{title} {description} {content}"

    #Extract Entities
    raw_entities = self.ner.extract_org_entities(text_blob)
    mapped_companies = self.entity_mapper.map_entities(raw_entities)

    #Score Sentiment
    sentiment_score = self.sentiment.score(text_blob)

    #Classify Type
    event_type = self.classify_event_type(text_blob)

    # Generate Id
    event_id = self.generate_event_id(title, str(published_at))

    return EventSchema(
      event_id=event_id,
      title=title,
      description=description,
      timestamp=str(published_at),
      sentiment=sentiment_score,
      event_type=event_type,
      mentioned_companies=mapped_companies,
    )
  
  def process_articles(self, articles: List[dict])->List[EventSchema]:
    events =[]
    # print(f"NLP Pipeline processing {len(articles)} raw articles...")
    for article in articles:
      try:
        if not article.get("title"):
          continue

        event=self.process_article(article)
        if event.mentioned_companies:
          events.append(event)
      except Exception as e:
        print(f"!!! Skipping article error: {e} !!! ")
        pass
    return events