from typing import Dict, Set, Tuple, Any
from app.db.neo4j_client import get_driver
from app.models.graph_dto import GraphNode, GraphEdge, GraphResponse

def _safe_props(props: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts Neo4j-specific types (like DateTime) into strings.
    """
    clean = {}
    for key, value in props.items():
        # If the value has an 'iso_format' method (like a Date), convert it to string
        if hasattr(value, "iso_format"):
            clean[key] = value.iso_format()
        else:
            clean[key] = value
    return clean


def get_company_subgraph(ticker: str) -> GraphResponse:
    """
    Fetches the subgraph centered around a company:
    [Events] -> (Company) -> (Sector)
    """
    driver = get_driver()

    query = """
    MATCH (c:Company {ticker: $ticker})
    OPTIONAL MATCH (c)-[:BELONGS_TO]->(s:Sector)
    OPTIONAL MATCH (e:Event)-[:AFFECTS]->(c)
    RETURN c, s, collect(e) AS events
    """

    with driver.session() as session:
        result = session.run(query, ticker=ticker)
        record = result.single()

    if not record or record["c"] is None:
        raise ValueError(f"Company {ticker} not found")

    nodes_map: Dict[str, GraphNode] = {}
    edges_set: Set[Tuple[str, str, str]] = set()

    # 1. Process Company Node
    c_node = record["c"]
    company_id = c_node["ticker"]
    nodes_map[company_id] = GraphNode(
        id=company_id,
        label="Company",
        properties=_safe_props(dict(c_node))  
    )

    # 2. Process Sector Node
    s_node = record["s"]
    if s_node:
        sector_id = s_node["name"]
        if sector_id not in nodes_map:
            nodes_map[sector_id] = GraphNode(
                id=sector_id,
                label="Sector",
                properties=_safe_props(dict(s_node)) 
            )
        edges_set.add((company_id, sector_id, "BELONGS_TO"))

    # 3. Process Event Nodes
    for e_node in record["events"]:
        if e_node:
            event_id = e_node["event_id"]
            if event_id not in nodes_map:
                nodes_map[event_id] = GraphNode(
                    id=event_id,
                    label="Event",
                    properties=_safe_props(dict(e_node)) 
                )
            edges_set.add((event_id, company_id, "AFFECTS"))

    return GraphResponse(
        nodes=list(nodes_map.values()),
        edges=[
            GraphEdge(source=s, target=t, type=rel)
            for s, t, rel in edges_set
        ]
    )