from services.data_loader import data_loader
from schemas.country import CountryOptions, CountryAnalysisResponse
from services.country_mapping import get_country_name, get_country_code
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

def get_country_options() -> CountryOptions:
    df = data_loader.get_resilience_metrics()
    
    # Map raw importer codes to validated names
    codes = df['importer'].dropna().unique()
    names = [get_country_name(c) for c in codes]
    countries = sorted(list(set(names)))
    
    commodities = sorted(df['commodity'].dropna().unique().tolist())
    years = sorted(df['year'].dropna().unique().tolist(), reverse=True)
    
    return CountryOptions(
        countries=countries,
        commodities=commodities,
        years=years
    )

def get_country_analysis(country: str, commodity: str, year: int) -> CountryAnalysisResponse:
    df = data_loader.get_resilience_metrics()
    
    # Resolve name back to code if passed name, or keep code if passed code
    importer_code = get_country_code(country)
    
    # Filter dataset by importer code
    filtered = df[
        (df['importer'].astype(str) == str(importer_code)) &
        (df['commodity'] == commodity) &
        (df['year'] == year)
    ]
    
    if len(filtered) == 0:
        raise HTTPException(status_code=404, detail="No validated FOODSHIELD observation is available for this country × commodity × year.")
        
    row = filtered.iloc[0]
    country_display_name = get_country_name(importer_code)
    
    return CountryAnalysisResponse(
        importer=country_display_name,
        commodity=str(row['commodity']),
        year=int(row['year']),
        baseline_imports=safe_float(row.get('baseline_imports')),
        supplier_count=int(row['supplier_count']),
        largest_supplier_share=safe_pct(row.get('largest_supplier_share')),
        top3_supplier_share=safe_pct(row.get('top3_supplier_share')),
        HHI=safe_float(row.get('HHI')),
        import_dependence=safe_pct(row.get('import_dependence')),
        
        lost_supply=safe_float(row.get('lost_supply')),
        shock_loss_share=safe_pct(row.get('shock_loss_share')),
        remaining_import_share=safe_pct(row.get('remaining_import_share')),
        
        replacement_rate=safe_pct(row.get('replacement_rate')),
        tier1_replacement=safe_float(row.get('tier1_replacement')),
        tier2_replacement=safe_float(row.get('tier2_replacement')),
        tier3_replacement=safe_float(row.get('tier3_replacement')),
        unreplaced_supply=safe_float(row.get('unreplaced_supply')),
        new_origin_share=safe_pct(row.get('new_origin_share')),
        
        resilience_profile=str(row['resilience_profile'])
    )
