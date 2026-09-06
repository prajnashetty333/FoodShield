from services.data_loader import data_loader
from schemas.sensitivity import SensitivityAnalysisResponse, SensitivitySummaryItem, ProfileTransitions
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

def get_sensitivity_analysis() -> SensitivityAnalysisResponse:
    df_summary = data_loader.get_sensitivity_summary()
    df_transitions = data_loader.get_sensitivity_transitions()
    
    summaries = []
    for _, row in df_summary.iterrows():
        summaries.append(
            SensitivitySummaryItem(
                experiment=str(row['experiment']),
                mean_replacement_rate=safe_pct(row.get('mean_replacement_rate')),
                type_A_share=safe_pct(row.get('type_A_share'))
            )
        )
        
    A_to_C = 0
    C_to_D = 0
    for _, row in df_transitions.iterrows():
        exp = str(row['experiment'])
        if '0.25' in exp:
            A_to_C = int(row.get('A_to_C', 0))
            C_to_D = int(row.get('C_to_D', 0))
            break
            
    return SensitivityAnalysisResponse(
        summaries=summaries,
        transitions_100_to_25=ProfileTransitions(
            A_to_C=A_to_C,
            C_to_D=C_to_D
        )
    )
