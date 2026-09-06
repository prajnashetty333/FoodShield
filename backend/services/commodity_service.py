from services.data_loader import data_loader
from schemas.commodity import CommodityAnalysisResponse, ProfileDistribution
from fastapi import HTTPException
import math

def safe_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        if math.isnan(f):
            return None
        return f
    except (ValueError, TypeError):
        return None

def safe_pct(val):
    f = safe_float(val)
    return None if f is None else f * 100.0

def get_commodity_analysis(commodity: str) -> CommodityAnalysisResponse:
    df = data_loader.get_resilience_metrics()
    
    filtered = df[df['commodity'] == commodity]
    
    total_scenarios = len(filtered)
    if total_scenarios == 0:
        raise HTTPException(status_code=404, detail=f"No validated observations available for commodity: {commodity}")
        
    mean_replacement_rate = filtered['replacement_rate'].mean()
    mean_shock_loss_share = filtered['shock_loss_share'].mean()
    mean_hhi = filtered['HHI'].mean()
    
    profile_counts = filtered['resilience_profile'].value_counts()
    
    def get_count(key):
        return int(profile_counts.get(key, 0))
        
    type_a = get_count("Existing-network resilient")
    type_b = get_count("Historically recoverable")
    type_c = get_count("New-origin dependent")
    type_d = get_count("Structurally constrained")
    
    return CommodityAnalysisResponse(
        commodity=commodity,
        total_scenarios=total_scenarios,
        mean_replacement_rate=safe_pct(mean_replacement_rate),
        mean_shock_loss_share=safe_pct(mean_shock_loss_share),
        mean_hhi=safe_float(mean_hhi),
        profile_distribution=[
            ProfileDistribution(profile="A", count=type_a, percentage=(type_a/total_scenarios)*100 if total_scenarios else 0.0),
            ProfileDistribution(profile="B", count=type_b, percentage=(type_b/total_scenarios)*100 if total_scenarios else 0.0),
            ProfileDistribution(profile="C", count=type_c, percentage=(type_c/total_scenarios)*100 if total_scenarios else 0.0),
            ProfileDistribution(profile="D", count=type_d, percentage=(type_d/total_scenarios)*100 if total_scenarios else 0.0),
        ]
    )
