from backend.services.data_loader import data_loader
from backend.schemas.shock import ShockAnalysisResponse
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

def get_shock_analysis(country: str, commodity: str, year: int, rank: int = 1) -> ShockAnalysisResponse:
    df = data_loader.get_supplier_shock()
    
    country_name = get_country_name(country)
    country_code = get_country_code(country)
    
    # Filter dataset
    filtered = df[
        ((df['importer_country_name'].astype(str) == str(country_name)) |
         (df['importer_country_code'].astype(str) == str(country_code))) &
        (df['commodity'] == commodity) &
        (df['year'] == year) &
        (df['supplier_rank'] == rank)
    ]
    
    if len(filtered) == 0:
        raise HTTPException(status_code=404, detail="No validated FOODSHIELD observation is available for this country × commodity × year × rank.")
        
    row = filtered.iloc[0]
    
    return ShockAnalysisResponse(
        importer=str(row.get('importer_country_name', country_name)),
        commodity=str(row['commodity']),
        year=int(row['year']),
        supplier_rank=int(row['supplier_rank']),
        shocked_supplier=str(row['supplier_country_name']),
        lost_supply_tonnes=safe_float(row.get('lost_supply_quantity_tonnes')),
        shock_loss_share=safe_pct(row.get('shock_loss_share')),
        remaining_import_share=safe_pct(row.get('remaining_import_share'))
    )
