import pandas as pd
import numpy as np
import json

print("Running validation tests...")

universe_df = pd.read_csv('data/processed/foodshield/foodshield_country_universe.csv')
expected_countries = set(universe_df['country_code'].unique())

metrics_df = pd.read_csv('data/processed/foodshield/foodshield_exposure_metrics_2010_2023.csv')
shares_df = pd.read_csv('data/processed/foodshield/foodshield_supplier_shares_2010_2023.csv')
exposure_old = pd.read_csv('data/processed/foodshield/foodshield_country_commodity_exposure_2010_2023.csv')

# Check A
present_countries = set(metrics_df['country_code'].unique())
absent_countries = expected_countries - present_countries
no_trade = universe_df[~universe_df['country_code'].isin(exposure_old['country_code'].unique())]['country_code'].tolist()
fbs_countries = set(metrics_df.dropna(subset=['domestic_supply'])['country_code'].unique())

# Check B
commodities = metrics_df['commodity'].unique().tolist()
assert len(commodities) == 6, f"Expected 6 commodities, got {len(commodities)}"

# Check C
years = metrics_df['year'].unique().tolist()
expected_years = list(range(2010, 2024))
assert set(years) == set(expected_years), f"Expected 2010-2023, got {years}"

# Check D
hhi_valid = metrics_df['hhi_0_1'].dropna().between(0, 1).all()

# Check E
shares_sum = shares_df.groupby(['country_code', 'commodity', 'year'])['quantity_share'].sum()
# Some might be slightly off due to float precision, so use np.isclose
shares_valid = np.isclose(shares_sum, 1.0, atol=1e-3).all()

# Check F
entropy_ge_0 = (metrics_df['supplier_entropy'].dropna() >= 0).all()
norm_entropy_valid = metrics_df['normalized_supplier_entropy'].dropna().between(0, 1).all()

# Check G
largest_valid = metrics_df['largest_supplier_share'].dropna().between(0, 1).all()

# Check H
top3_valid = metrics_df['top3_supplier_share'].dropna().between(0, 1).all()
top5_valid = metrics_df['top5_supplier_share'].dropna().between(0, 1).all()
top_logic = (metrics_df['top5_supplier_share'] >= metrics_df['top3_supplier_share']).all() and (metrics_df['top3_supplier_share'] >= metrics_df['largest_supplier_share']).all()

# Check I
m_totals = metrics_df[['country_code', 'commodity', 'year', 'total_import_quantity_tonnes', 'total_import_value_1000_usd']]
o_totals = exposure_old[['country_code', 'commodity', 'year', 'total_import_quantity_tonnes', 'total_import_value_1000_usd']]
merged = m_totals.merge(o_totals, on=['country_code', 'commodity', 'year'], suffixes=('_new', '_old'))
qty_match = np.isclose(merged['total_import_quantity_tonnes_new'].fillna(0), merged['total_import_quantity_tonnes_old'].fillna(0), atol=1e-3).all()
val_match = np.isclose(merged['total_import_value_1000_usd_new'].fillna(0), merged['total_import_value_1000_usd_old'].fillna(0), atol=1e-3).all()

# Missingness
missing_stats = metrics_df.isnull().sum().to_dict()
missing_by_comm = metrics_df.groupby('commodity').apply(lambda x: x.isnull().sum()).to_dict('index')

results = {
    'Check A': {
        'universe_count': len(expected_countries),
        'present_count': len(present_countries),
        'absent_count': len(absent_countries),
        'no_trade_count': len(no_trade),
        'fbs_countries_count': len(fbs_countries)
    },
    'Check B': {'commodities': commodities, 'count': len(commodities)},
    'Check C': {'min_year': min(years), 'max_year': max(years), 'count': len(years)},
    'Check D': {'hhi_valid': bool(hhi_valid)},
    'Check E': {'shares_sum_valid': bool(shares_valid)},
    'Check F': {'entropy_ge_0': bool(entropy_ge_0), 'norm_entropy_valid': bool(norm_entropy_valid)},
    'Check G': {'largest_share_valid': bool(largest_valid)},
    'Check H': {'top_shares_valid': bool(top3_valid and top5_valid), 'logic_valid': bool(top_logic)},
    'Check I': {'quantity_match': bool(qty_match), 'value_match': bool(val_match)},
    'Missingness': missing_stats,
    'Missingness_by_comm': missing_by_comm
}

with open('scratch/validation_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Validation complete.")
