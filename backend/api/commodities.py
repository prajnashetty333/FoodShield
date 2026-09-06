from fastapi import APIRouter
from services.commodity_service import get_commodity_analysis
from schemas.commodity import CommodityAnalysisResponse
from typing import List
import backend.config as cfg

router = APIRouter()

@router.get("", response_model=List[str])
def list_commodities():
    return cfg.LOCKED_COMMODITIES

@router.get("/analysis", response_model=CommodityAnalysisResponse)
def read_commodity_analysis(commodity: str):
    return get_commodity_analysis(commodity)
