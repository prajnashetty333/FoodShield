from pydantic import BaseModel
from typing import Optional, List, Dict

class ProfileTransitions(BaseModel):
    A_to_C: int
    C_to_D: int

class SensitivitySummaryItem(BaseModel):
    experiment: str
    mean_replacement_rate: Optional[float]
    type_A_share: Optional[float]
    
class SensitivityAnalysisResponse(BaseModel):
    summaries: List[SensitivitySummaryItem]
    transitions_100_to_25: ProfileTransitions
