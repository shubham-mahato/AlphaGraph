import os
import sys
from typing import List
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv
from nlp_services.schemas.event_schema import EventSchema

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

load_dotenv(ROOT_DIR/"backend"/".env")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

class EventGraphWriter:
  def __init__(self):
    self.driver = GraphDatabase.driver(
      NEO4J_URI,
      auth = (NEO4J_USER,NEO4J_PASSWORD)
    )
  def close(self):
    self.driver.close()
  def write_events(self, events: List[EventSchema]):
    print(f"Connecting to Neo4j to write {len(events)} events...")
    with self.driver.session() as session:
      for event in events:
        try:
          self._write_single_event(session,event)
        except Exception as e:
          print(f"Failed to write event {event.event_id}: {e}")
  def _write_single_event(self,session,event:EventSchema):
    if not event.mentioned_companies:
      return
    # 1. Merge the Event Node (Idempotent)
    session.run(
    """
      MERGE (e:Event {event_id: $event_id})
      SET e.title = $title,
          e.description = $description,
          e.timestamp = datetime($timestamp),
          e.sentiment = $sentiment,
          e.event_type = $event_type,
          e.source = 'NewsAPI'
    """,
    event_id=event.event_id,
    title=event.title,
    description=event.description,
    timestamp=event.timestamp, 
    sentiment=event.sentiment,
    event_type=event.event_type,
  )
  # 2. Link to Companies

    for ticker in event.mentioned_companies:
      session.run(
        """
        MATCH (e:Event {event_id: $event_id})
        MATCH (c:Company {ticker: $ticker})
        MERGE (e)-[:AFFECTS]->(c)
        """,
        event_id= event.event_id,
        ticker=ticker,
      )