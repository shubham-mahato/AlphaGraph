from fastapi import APIRouter, HTTPException
from app.models.graph_dto import GraphResponse
from app.services.graph_service import get_company_subgraph

router = APIRouter(
  prefix = "/graph",
  tags= ["Graph Visualization"]
)

@router.get("/company/{ticker}", response_model=GraphResponse)
async def company_subgraph(ticker:str):
  """
    Get the graph topology (nodes & edges) for a specific company.
    Ideal for rendering force-directed graphs.
  """
  try:
    return get_company_subgraph(ticker.upper())
  except ValueError:
    raise HTTPException(status_code=404, detail="Company not Found")