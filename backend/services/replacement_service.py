from backend.services.data_loader import data_loader
from backend.schemas.replacement import ReplacementAnalysisResponse
from backend.services.country_mapping import get_country_name, get_country_code
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

def get_replacement_analysis(country: str, commodity: str, year: int, rank: int = 1) -> ReplacementAnalysisResponse:
    df = data_loader.get_replacement_results()
    
    country_name = get_country_name(country)
    country_code = get_country_code(country)
    
    # Filter dataset matching either importer_country_name or importer_country_code
    filtered = df[
        ((df['importer_country_name'].astype(str) == str(country_name)) |
         (df['importer_country_code'].astype(str) == str(country_code))) &
        (df['commodity'] == commodity) &
        (df['year'] == year) &
        (df['shock_rank'] == rank)
    ]
    
    if len(filtered) == 0:
        raise HTTPException(status_code=404, detail="No validated FOODSHIELD observation is available for this country × commodity × year × rank.")
        
    row = filtered.iloc[0]
    
    return ReplacementAnalysisResponse(
        importer=str(row.get('importer_country_name', country_name)),
        commodity=str(row['commodity']),
        year=int(row['year']),
        shock_rank=int(row['shock_rank']),
        shocked_supplier=str(row['shocked_supplier']),
        lost_supply=safe_float(row.get('lost_supply')),
        tier1_replacement=safe_float(row.get('tier1_replacement')),
        tier2_replacement=safe_float(row.get('tier2_replacement')),
        tier3_replacement=safe_float(row.get('tier3_replacement')),
        unreplaced_supply=safe_float(row.get('unreplaced_supply')),
        replacement_rate=safe_pct(row.get('replacement_rate')),
        new_origin_share=safe_pct(row.get('new_origin_share')),
        outcome_type=str(row['outcome_type']),
        capacity_status=str(row['capacity_status'])
    )
