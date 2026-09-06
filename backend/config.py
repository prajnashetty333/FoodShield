import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "processed" / "foodshield"

# Specific File Paths
FILE_RESILIENCE_METRICS = DATA_DIR / "foodshield_resilience_metrics_2010_2023.csv"
FILE_RESEARCH_FINDINGS = DATA_DIR / "foodshield_research_findings_2010_2023.csv"
FILE_COMMODITY_FINDINGS = DATA_DIR / "foodshield_commodity_findings_2010_2023.csv"
FILE_COUNTRY_FINDINGS = DATA_DIR / "foodshield_country_findings_2010_2023.csv"
FILE_REPLACEMENT_RESULTS = DATA_DIR / "foodshield_replacement_results_2010_2023.csv"
FILE_REPLACEMENT_SUMMARY = DATA_DIR / "foodshield_replacement_summary_2010_2023.csv"
FILE_SUPPLIER_SHOCK = DATA_DIR / "foodshield_supplier_shock_2010_2023.csv"
FILE_SHOCK_SUMMARY = DATA_DIR / "foodshield_shock_summary_2010_2023.csv"
FILE_EXPOSURE_METRICS = DATA_DIR / "foodshield_exposure_metrics_2010_2023.csv"
FILE_SENSITIVITY_SUMMARY = DATA_DIR / "foodshield_sensitivity_summary_2010_2023.csv"
FILE_SENSITIVITY_TRANSITIONS = DATA_DIR / "foodshield_sensitivity_profile_transitions_2010_2023.csv"
FILE_SENSITIVITY_TYPE_C = DATA_DIR / "foodshield_sensitivity_type_c_2010_2023.csv"

# Locked Constraints
LOCKED_COMMODITIES = [
    "Wheat",
    "Rice",
    "Maize",
    "Palm Oil",
    "Sugar",
    "Sunflower Oil"
]
LOCKED_YEARS = list(range(2011, 2024))
DEFAULT_SHOCK_RANK = 1

# Profile Colors
PROFILE_COLORS = {
    "A": "green",
    "B": "blue",
    "C": "orange",
    "D": "red"
}
