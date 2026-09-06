from fastapi import APIRouter
from services.country_service import get_country_options, get_country_analysis
from schemas.country import CountryOptions, CountryAnalysisResponse

router = APIRouter()

@router.get("/options", response_model=CountryOptions)
def read_country_options():
    return get_country_options()

@router.get("/analysis", response_model=CountryAnalysisResponse)
def read_country_analysis(country: str, commodity: str, year: int):
    return get_country_analysis(country, commodity, year)
