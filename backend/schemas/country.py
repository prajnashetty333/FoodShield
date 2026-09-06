from pydantic import BaseModel
from typing import List, Optional

class CountryOptions(BaseModel):
    countries: List[str]
    commodities: List[str]
    years: List[int]

class CountryAnalysisResponse(BaseModel):
    importer: str
    commodity: str
    year: int
    baseline_imports: Optional[float]
    supplier_count: int
    largest_supplier_share: Optional[float]
    top3_supplier_share: Optional[float]
    HHI: Optional[float]
    import_dependence: Optional[float]
    
    # Shock metrics
    lost_supply: Optional[float]
    shock_loss_share: Optional[float]
    remaining_import_share: Optional[float]
    
    # Replacement metrics
    replacement_rate: Optional[float]
    tier1_replacement: Optional[float]
    tier2_replacement: Optional[float]
    tier3_replacement: Optional[float]
    unreplaced_supply: Optional[float]
    new_origin_share: Optional[float]
    
    resilience_profile: str
