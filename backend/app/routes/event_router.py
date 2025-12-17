from fastapi import APIRouter,HTTPException
from app.services.event_service import get_event_details, EventResponse

router = APIRouter(prefix="/event",tags=["Event"])

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id:str):
  """
  Fetch a specific event and the companies it impacts.
  """
  data = get_event_details(event_id)

  if not data:
    raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")
  
  return data