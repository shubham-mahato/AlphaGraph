from typing import List, Optional
from pydantic import BaseModel

class EventSchema(BaseModel):
  event_id: str
  title: str
  description: Optional[str] =None
  timestamp: Optional[str] =None
  sentiment:float
  event_type: str
  mentioned_companies: List[str]
