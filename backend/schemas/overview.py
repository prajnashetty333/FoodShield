from pydantic import BaseModel
from typing import Optional, List, Dict

class ProfileDistribution(BaseModel):
    profile: str
    count: int
    percentage: Optional[float]

class OverviewResponse(BaseModel):
    total_scenarios: int
    mean_replacement_rate: Optional[float]
    type_a_percentage: Optional[float]
    type_c_percentage: Optional[float]
    profile_distribution: List[ProfileDistribution]
