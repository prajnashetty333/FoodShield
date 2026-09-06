from typing import Optional
from pydantic import BaseModel

class ReplacementAnalysisResponse(BaseModel):
    importer: str
    commodity: str
    year: int
    shock_rank: int
    shocked_supplier: str
    lost_supply: Optional[float]
    tier1_replacement: Optional[float]
    tier2_replacement: Optional[float]
    tier3_replacement: Optional[float]
    unreplaced_supply: Optional[float]
    replacement_rate: Optional[float]
    new_origin_share: Optional[float]
    outcome_type: str
    capacity_status: str
