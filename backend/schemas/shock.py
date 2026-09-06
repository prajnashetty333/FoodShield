from pydantic import BaseModel
from typing import List, Optional

class ShockAnalysisResponse(BaseModel):
    importer: str
    commodity: str
    year: int
    supplier_rank: int
    shocked_supplier: str
    lost_supply_tonnes: Optional[float]
    shock_loss_share: Optional[float]
    remaining_import_share: Optional[float]
