from fastapi import APIRouter
from backend.services.overview_service import get_overview_metrics
from backend.schemas.overview import OverviewResponse

router = APIRouter()

@router.get("", response_model=OverviewResponse)
def get_overview():
    return get_overview_metrics()
