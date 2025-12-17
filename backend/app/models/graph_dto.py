from typing import Dict, List ,Any
from pydantic import BaseModel

class GraphNode(BaseModel):
  id: str
  label: str
  properties : Dict[str,Any]

class GraphEdge(BaseModel):
  source:str
  target:str
  type:str

class GraphResponse(BaseModel):
  nodes: List[GraphNode]
  edges: List[GraphEdge]
