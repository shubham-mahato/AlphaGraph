from fastapi import APIRouter,HTTPException
from app.services.company_service import get_company_details
from app.models.company import CompanyResponse

router = APIRouter(prefix="/company",tags=["Company"])

@router.get("/{ticker}", response_model=CompanyResponse)
async def get_company(ticker:str):
  """
    Fetch a company and its recent events by Ticker (e.g., TCS).
  """
  data = get_company_details(ticker.upper())

  if not data:
    raise HTTPException(status_code=404,detail=f"Company '{ticker}' not found.")
  return data