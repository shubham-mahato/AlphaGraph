from typing import List
from neo4j import Driver
from app.db.neo4j_client import get_driver
from app.models.shock import ShockImpact,ShockResponse

# 0.6 means 60% of the shock transfers to the next node
DECAY_FACTOR = 0.6

def run_shock_simulation(event_id:str)->ShockResponse:
  driver:Driver = get_driver()

  # Query 1: Get the Event's base sentiment and the directly hit companies
  query_direct = """
  MATCH (e:Event {event_id: $event_id})-[:AFFECTS]->(c:Company)
  RETURN e.sentiment AS sentiment, collect(c) AS companies
  """
  with driver.session() as session:
    record = session.run(query_direct,event_id=event_id).single()
  
  if not record:
    raise ValueError(f"Event {event_id} not found or has no connections")
  
  base_sentiment = record["sentiment"]
  direct_companies = record["companies"]

  impacts: List[ShockImpact] = []

  # --- Calculation 1: Direct Impact (Distance = 1) ---

  for c in direct_companies:
    # Formula: Sentiment * (0.6 ^ 1)
    score = base_sentiment + (DECAY_FACTOR **1)
    impacts.append(
      ShockImpact(
        node_id=c["ticker"],
        node_type="Company",
        distance=1,
        impact_score=score
      )
    )

  # --- Calculation 2: Sector Contagion (Distance = 3) ---
  # Path: Event -> Company -> Sector -> PeerCompany
  query_peers = """
      MATCH (e:Event {event_id: $event_id})-[:AFFECTS]->(c1:Company)
      MATCH (c1)-[:BELONGS_TO]->(s:Sector)<-[:BELONGS_TO]-(c2:Company)
      WHERE c2 <> c1
      RETURN DISTINCT c2
  """
  with driver.session() as session:
    result = session.run(query_peers,event_id=event_id)

    for record in result:
      peer = record["c2"]
      # Formula: Sentiment * (0.6 ^ 3) -> Much weaker impact
      score = base_sentiment * (DECAY_FACTOR ** 3)
      impacts.append(
        ShockImpact(
          node_id=peer["ticker"],
          node_type="Company",
          distance=3,
          impact_score=score
        )
      )
  return ShockResponse(
        event_id=event_id,
        base_sentiment=base_sentiment,
        impacts=impacts
  )
