from pydantic import BaseModel
from typing import Optional, List

#Basic Company Model
class Company(BaseModel):
  ticker:str
  name:str
  sector:Optional[str]=None
  country:Optional[str]=None

#Basic Event Model
class Event(BaseModel):
  event_id:str
  title: str
  sentiment: Optional[str]=None
  timestamp:Optional[str] = None
  event_type:Optional[str]=None

#Response Model: Company + Event List
class CompanyResponse(BaseModel):
  company: Company
  events:List[Event]
