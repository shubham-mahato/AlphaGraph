from typing import Dict,Set,Tuple
from app.db.neo4j_client import get_driver
from app.models.graph_dto import GraphEdge,GraphNode,GraphResponse

def get_company_subgraph(ticker:str) -> GraphResponse:
  """
    Fetches the subgraph centered around a company:
    [Events] -> (Company) -> (Sector)
  """
  driver = get_driver()

# Cypher: Find company, optionally its sector, optionally impacting events
  query = """
    MATCH (c:Company {ticker: $ticker})
    OPTIONAL MATCH (c)-[:BELONGS_TO]->(s:Sector)
    OPTIONAL MATCH (e:Event)-[:AFFECTS]->(c)
    RETURN c, s, collect(e) AS events
    """
  with driver.session() as session:
    result = session.run(query,ticker=ticker)
    record = session.single()
  
  if not record or record["c"] is None:
    raise ValueError(f"Company {ticker} not found")
  
  # Deduplication Container
  nodes_map: Dict[str, GraphNode] ={}
  edges_set: Set[Tuple[str,str,str]] = set()

  # 1. Process Company Node
  c_node = record["c"]
  company_id = c_node["ticker"]
  nodes_map[company_id] = GraphNode(
    id = company_id,
    label="Company",
    properties=dict(c_node)
  )
  # 2. Process Sector Node
  s_node = record["s"]
  if s_node:
    sector_id = s_node["name"]
    if sector_id not in nodes_map:
      nodes_map[sector_id] = GraphNode(
        id = sector_id,
        label= "Sector",
        properties=dict(s_node)
      )
    # Edge: Company-> Sector
    edges_set.add((company_id,sector_id,"BELONGS_TO"))
  
  # 3. Process event node 
  for e_node in record["events"]:
    if e_node:
      event_id =e_node["event_id"]
      if event_id not in nodes_map:
        nodes_map[event_id] = GraphNode(
          id = event_id,
          label="event",
          properties=dict(e_node)
        )
      #Edge: Event->Company
      edges_set.add((event_id,company_id,"AFFECTS"))
  
  # 4. Construct Response
  return GraphResponse(
    nodes=list(nodes_map.values()),
    edges=[
      GraphEdge(source=s, target=t,type=rel)
      for s,t,rel in edges_set
    ]
  )
