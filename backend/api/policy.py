from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class PolicyRecommendation(BaseModel):
    profile: str
    name: str
    directions: List[str]

class PolicyResponse(BaseModel):
    framework: List[PolicyRecommendation]
    disclaimer: str

@router.get("", response_model=PolicyResponse)
def read_policy():
    return PolicyResponse(
        framework=[
            PolicyRecommendation(
                profile="A",
                name="Current-network resilient",
                directions=[
                    "maintain supplier diversification",
                    "monitor concentration",
                    "preserve functioning supplier relationships",
                    "periodically reassess exposure"
                ]
            ),
            PolicyRecommendation(
                profile="B",
                name="Historically recoverable",
                directions=[
                    "preserve/revive historical supplier relationships",
                    "maintain market access",
                    "investigate supplier re-entry feasibility"
                ]
            ),
            PolicyRecommendation(
                profile="C",
                name="New-origin dependent",
                directions=[
                    "develop additional origins",
                    "diversify sourcing geography",
                    "investigate market-access diversification",
                    "qualify alternative origins in real-world settings"
                ]
            ),
            PolicyRecommendation(
                profile="D",
                name="Structurally constrained",
                directions=[
                    "investigate structural constraints",
                    "examine logistics",
                    "infrastructure",
                    "trade policy",
                    "contracts",
                    "storage",
                    "transport",
                    "geopolitical exposure",
                    "domestic contingency options"
                ]
            )
        ],
        disclaimer="These factors are not necessarily modeled. These are decision-support implications of the modeled trade-replacement framework, not forecasts, causal conclusions, or guarantees of real-world food security."
    )
