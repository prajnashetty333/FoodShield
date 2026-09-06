from fastapi import APIRouter, Query
from backend.services.shock_service import get_shock_analysis
from backend.schemas.shock import ShockAnalysisResponse

router = APIRouter()

@router.get("/analysis", response_model=ShockAnalysisResponse)
def read_shock_analysis(
    country: str, 
    commodity: str, 
    year: int,
    rank: int = Query(1, description="Supplier Rank (1, 2, or 3)")
):
    return get_shock_analysis(country, commodity, year, rank)
