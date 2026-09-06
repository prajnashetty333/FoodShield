from fastapi import APIRouter
from services.sensitivity_service import get_sensitivity_analysis
from schemas.sensitivity import SensitivityAnalysisResponse

router = APIRouter()

@router.get("/analysis", response_model=SensitivityAnalysisResponse)
def read_sensitivity_analysis():
    return get_sensitivity_analysis()
