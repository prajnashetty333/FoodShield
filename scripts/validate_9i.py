import pandas as pd
import json
import sys

LOCKED_YEARS = list(range(2011, 2024))
LOCKED_COMMODITIES = ['Wheat', 'Rice', 'Maize', 'Palm Oil', 'Sugar', 'Sunflower Oil']

# Load primary dataset
df = pd.read_csv('data/processed/foodshield/foodshield_resilience_metrics_2010_2023.csv')
primary = df[
    (df['shock_rank'] == 1) &
    (df['year'].isin(LOCKED_YEARS)) &
    (df['commodity'].isin(LOCKED_COMMODITIES)) &
    (df['capacity_status'] == 'capacity_available')
]

total = len(primary)
profiles = primary['resilience_profile'].value_counts().to_dict()
mean_replacement = primary['replacement_rate'].mean()
mean_shock_loss = primary['shock_loss_share'].mean()

print("=== PRIMARY SCOPE VALIDATION ===")
print(f"Total scenarios: {total} (expected 10953)")
print(f"Profile A: {profiles.get('A', 0)} (expected 9534)")
print(f"Profile B: {profiles.get('B', 0)} (expected 438)")
print(f"Profile C: {profiles.get('C', 0)} (expected 936)")
print(f"Profile D: {profiles.get('D', 0)} (expected 45)")
print(f"A+B+C+D = {sum(profiles.values())} (should equal {total})")
print(f"Mean replacement rate: {mean_replacement:.4f} (expected ~0.9983)")
print(f"Mean shock loss share: {mean_shock_loss:.4f} (expected ~0.6717)")

# Sankey reconciliation check
print("\n=== SANKEY RECONCILIATION ===")
rdf = pd.read_csv('data/processed/foodshield/foodshield_replacement_results_2010_2023.csv')
rprimary = rdf[
    (rdf['shock_rank'] == 1) &
    (rdf['year'].isin(LOCKED_YEARS)) &
    (rdf['commodity'].isin(LOCKED_COMMODITIES)) &
    (rdf['capacity_status'] == 'capacity_available')
]
rprimary = rprimary.copy()
rprimary['computed_sum'] = rprimary['tier1_replacement'] + rprimary['tier2_replacement'] + rprimary['tier3_replacement'] + rprimary['unreplaced_supply']
rprimary['diff'] = (rprimary['computed_sum'] - rprimary['lost_supply']).abs()
within_tolerance = (rprimary['diff'] < 1.0).mean() * 100
print(f"Rows where tier1+tier2+tier3+unreplaced == lost_supply (within 1 tonne): {within_tolerance:.2f}%")

# Country mapping check
from backend.services.country_mapping import COUNTRY_MAPPING
unique_codes = primary['importer'].astype(str).unique()
unmapped = [c for c in unique_codes if c not in COUNTRY_MAPPING]
print(f"\n=== COUNTRY MAPPING ===")
print(f"Total unique importer codes: {len(unique_codes)}")
print(f"Unmapped codes: {len(unmapped)}")
if unmapped[:5]:
    print(f"Sample unmapped: {unmapped[:5]}")

# Sensitivity check
print("\n=== SENSITIVITY VALIDATION ===")
sdf = pd.read_csv('data/processed/foodshield/foodshield_sensitivity_summary_2010_2023.csv')
print(sdf[['experiment', 'mean_replacement_rate', 'type_A_share']].to_string())

# Source CSV immutability check
import os
csv_files = [
    'data/processed/foodshield/foodshield_resilience_metrics_2010_2023.csv',
    'data/processed/foodshield/foodshield_replacement_results_2010_2023.csv',
    'data/processed/foodshield/foodshield_supplier_shock_2010_2023.csv',
    'data/processed/foodshield/foodshield_sensitivity_summary_2010_2023.csv',
]
print("\n=== SOURCE CSV IMMUTABILITY ===")
for f in csv_files:
    stat = os.stat(f)
    print(f"{f}: size={stat.st_size}, mtime={stat.st_mtime}")
