from typing import List
from pydantic import BaseModel

class ShockImpact(BaseModel):
  node_id: str
  node_type: str      # "Company" | "Sector"
  distance: int       # 1 = Direct, 3 = Peer (via Sector)
  impact_score: float

class ShockResponse(BaseModel):
  event_id: str
  base_sentiment: float
  impacts: List[ShockImpact]
