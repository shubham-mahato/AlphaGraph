from typing import Optional
from neo4j import Driver
from app.db.neo4j_client import get_driver
from app.models.company import Company,Event,CompanyResponse

def get_company_details(ticker:str) ->Optional[CompanyResponse]:
  driver:Driver = get_driver()
  
  query = """
    MATCH (c:Company {ticker: $ticker})
    OPTIONAL MATCH (e:Event)-[:AFFECTS]->(c)
    RETURN c, collect(e) as events
    """
  with driver.session() as session:
    result = session.run(query,ticker=ticker)
    record =result.single()
  
  if not record or record["c"] is None:
    return None
  
  #Map Neo4j Node to Pydantic Model
  company_node = record["c"]
  company_data = Company(
    ticker=company_node.get("ticker"),
    name=company_node.get("name"),
    sector=company_node.get("sector"),
    country=company_node.get("country")
  )

  #Map Event
  event_list =[]
  for evt in record["events"]:
    if evt:
      event_list.append(Event(
        event_id=evt.get("event_id"),
        title=evt.get("title"),
        sentiment=evt.get("sentiment"),
        timestamp=str(evt.get("timestamp")),
        event_type=evt.get("event_type")
      ))
  return CompanyResponse(company=company_data,events=event_list)
