from pydantic import BaseModel
from typing import Optional, List

class ProfileDistribution(BaseModel):
    profile: str
    count: int
    percentage: Optional[float]

class CommodityAnalysisResponse(BaseModel):
    commodity: str
    total_scenarios: int
    mean_replacement_rate: Optional[float]
    mean_shock_loss_share: Optional[float]
    mean_hhi: Optional[float]
    profile_distribution: List[ProfileDistribution]
