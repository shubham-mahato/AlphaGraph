from typing import Optional,List
from neo4j import Driver
from app.db.neo4j_client import get_driver
from app.models.company import Event,Company
from pydantic import BaseModel

# Response model for Event + Affected Companies
class EventResponse(BaseModel):
  event: Event
  affected_companies: List[Company]

def get_event_details(event_id:str)->Optional[EventResponse]:
  driver:Driver = get_driver()

  query = """
    MATCH (e:Event {event_id: $event_id})
    OPTIONAL MATCH (e)-[:AFFECTS]->(c:Company)
    RETURN e, collect(c) as companies
    """
  
  with driver.session() as session:
    result = session.run(query, event_id=event_id)
    record = result.single()
  
  if not record or record["e"] is None:
    return None

  # Map event Node
  event_node = record["e"]
  event_data = Event(
    event_id=event_node.get("event_id"),
    title=event_node.get("title"),
    sentiment=event_node.get("sentiment"),
    timestamp=str(event_node.get("timestamp")),
    event_type=event_node.get("event_type")
  ) 

  # Map Companies 
  company_list = []
  for comp in record["companies"]:
    if comp:
      company_list.append(Company(
        ticker=comp.get("ticker"),
        name=comp.get("name"),
        sector=comp.get("sector"),
        country=comp.get("country")
      ))

  return EventResponse(event=event_data, affected_companies=company_list)