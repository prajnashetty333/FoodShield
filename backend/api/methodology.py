from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MethodologyResponse(BaseModel):
    limitations: List[str]
    disclaimer: str

@router.get("", response_model=MethodologyResponse)
def read_methodology():
    return MethodologyResponse(
        limitations=[
            "actual future availability",
            "guaranteed spare capacity",
            "prices",
            "transport constraints",
            "logistics",
            "infrastructure",
            "policy response",
            "geopolitical behavior",
            "contracts",
            "storage",
            "future supplier behavior",
            "causal effects",
            "consumer-level food insecurity",
            "cross-food substitution"
        ],
        disclaimer="FOODSHIELD models trade-replacement feasibility under historical trade relationships and a historical export-expansion capacity proxy. It does not predict or guarantee real-world food security."
    )
