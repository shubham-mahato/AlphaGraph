from fastapi import APIRouter,HTTPException
from app.models.shock import ShockResponse
from app.services.shock_service import run_shock_simulation

router = APIRouter(
    prefix="/shock",
    tags=["Shock Engine"]
)

@router.get("/{event_id}",response_model=ShockResponse)
async def simulate_shock(event_id: str):
  """
    Triggers a propagation algorithm to calculate how a specific event
    ripples through the market graph.
  """
  try: 
    return run_shock_simulation(event_id)
  except ValueError as e:
    raise HTTPException(status_code=404, detail=str(e))
  except Exception as e:
    print(f"Error: {e}")
    raise HTTPException(status_code=500, detail="Simulation Failed")
