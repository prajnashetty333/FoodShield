from fastapi import APIRouter, Query
from services.replacement_service import get_replacement_analysis
from schemas.replacement import ReplacementAnalysisResponse

router = APIRouter()

@router.get("/analysis", response_model=ReplacementAnalysisResponse)
def read_replacement_analysis(
    country: str, 
    commodity: str, 
    year: int,
    rank: int = Query(1, description="Supplier Rank")
):
    return get_replacement_analysis(country, commodity, year, rank)
