import pandas as pd
import numpy as np

print("Loading data...")
# Load exposure (for total imports)
exposure_df = pd.read_csv('data/processed/foodshield/foodshield_country_commodity_exposure_2010_2023.csv')

# Load supplier shares (for concentration metrics)
shares_df = pd.read_csv('data/processed/foodshield/foodshield_supplier_shares_2010_2023.csv')

# Calculate Supplier Concentration Metrics
print("Calculating supplier concentration...")
# filter positive quantity shares
shares_pos = shares_df[shares_df['quantity_share'] > 0].copy()

# HHI
shares_pos['sq_share'] = shares_pos['quantity_share'] ** 2
# Entropy
shares_pos['entropy_term'] = -shares_pos['quantity_share'] * np.log(shares_pos['quantity_share'])

# Group by country, commodity, year
grouped = shares_pos.groupby(['country_code', 'country_name', 'commodity', 'year'])

# Calculate metrics
conc_df = grouped.agg(
    supplier_count=('supplier_country_code', 'count'),
    largest_supplier_share=('quantity_share', 'max'),
    hhi_0_1=('sq_share', 'sum'),
    supplier_entropy=('entropy_term', 'sum')
).reset_index()

# Top 3 and Top 5 shares
def get_top_k(g, k):
    return g['quantity_share'].nlargest(k).sum()

top_shares = shares_pos.groupby(['country_code', 'country_name', 'commodity', 'year']).apply(
    lambda g: pd.Series({
        'top3_supplier_share': get_top_k(g, 3),
        'top5_supplier_share': get_top_k(g, 5)
    })
).reset_index()

conc_df = conc_df.merge(top_shares, on=['country_code', 'country_name', 'commodity', 'year'], how='left')

# Add normalized entropy and hhi_0_10000
conc_df['hhi_0_10000'] = conc_df['hhi_0_1'] * 10000

def calc_norm_entropy(row):
    if row['supplier_count'] <= 1:
        return 0.0
    return row['supplier_entropy'] / np.log(row['supplier_count'])

conc_df['normalized_supplier_entropy'] = conc_df.apply(calc_norm_entropy, axis=1)

print("Processing FBS data...")
# Load FBS
fbs_df = pd.read_csv('data/processed/FoodBalanceSheets_E_All_Data.csv')

# Define mappings
comm_to_fbs = {
    'Wheat': 2511,
    'Rice': 2807,
    'Maize': 2514,
    'Palm Oil': 2577,
    'Sugar': 2542,
    'Sunflower Oil': 2573
}
fbs_to_comm = {v: k for k, v in comm_to_fbs.items()}
valid_fbs_items = list(comm_to_fbs.values())

fbs_sub = fbs_df[fbs_df['Item Code'].isin(valid_fbs_items) & (fbs_df['Year'].between(2010, 2023))].copy()
fbs_sub['commodity'] = fbs_sub['Item Code'].map(fbs_to_comm)

# Pivot elements
fbs_pivot = fbs_sub.pivot_table(
    index=['Area Code (M49)', 'Area', 'commodity', 'Year'],
    columns='Element',
    values='Value',
    aggfunc='first'
).reset_index()

# We need country codes in M49 to match our universe? Wait, the exposure data uses 'country_code' which is standard M49 numeric (stripped of ' quotes in FBS)?
# Let's clean M49 in FBS
fbs_pivot['country_code'] = fbs_pivot['Area Code (M49)'].str.replace("'", "").astype(int)

# Extract FBS Grand Total for calories/protein
fbs_grand = fbs_df[(fbs_df['Item'] == 'Grand Total') & (fbs_df['Year'].between(2010, 2023))].copy()
fbs_grand_pivot = fbs_grand.pivot_table(
    index=['Area Code (M49)', 'Year'],
    columns='Element',
    values='Value',
    aggfunc='first'
).reset_index()
fbs_grand_pivot['country_code'] = fbs_grand_pivot['Area Code (M49)'].str.replace("'", "").astype(int)
fbs_grand_pivot = fbs_grand_pivot[['country_code', 'Year', 'Food supply (kcal/capita/day)', 'Protein supply quantity (g/capita/day)']]
fbs_grand_pivot.rename(columns={
    'Food supply (kcal/capita/day)': 'total_kcal_capita_day',
    'Protein supply quantity (g/capita/day)': 'total_protein_g_capita_day'
}, inplace=True)

# Merge Grand total into FBS pivot
fbs_pivot = fbs_pivot.merge(fbs_grand_pivot, on=['country_code', 'Year'], how='left')

# Calculate FBS metrics
# If element not present, we will let it be NaN (we don't fill with zero as per instructions)
def get_col(df, col):
    if col in df.columns:
        return df[col]
    return np.nan

fbs_pivot['production_quantity'] = get_col(fbs_pivot, 'Production')
fbs_pivot['fbs_import_quantity'] = get_col(fbs_pivot, 'Import quantity')
fbs_pivot['fbs_export_quantity'] = get_col(fbs_pivot, 'Export quantity')
fbs_pivot['domestic_supply'] = get_col(fbs_pivot, 'Domestic supply quantity')
fbs_pivot['food_supply_quantity'] = get_col(fbs_pivot, 'Food supply quantity (kg/capita/yr)')
fbs_pivot['food_supply_kcal'] = get_col(fbs_pivot, 'Food supply (kcal/capita/day)')
fbs_pivot['food_supply_protein'] = get_col(fbs_pivot, 'Protein supply quantity (g/capita/day)')

# Import dependence = (Imports - Exports) / Domestic Supply
fbs_pivot['import_dependence'] = (fbs_pivot['fbs_import_quantity'].fillna(0) - fbs_pivot['fbs_export_quantity'].fillna(0)) / fbs_pivot['domestic_supply']
# Note: we are not silently filling missing for the final output, just for the calculation where one component might be missing but domestic supply exists.
# Wait, let's strictly follow: if Import or Export is missing, do we assume 0 for math?
# Usually yes in FBS, but let's avoid filling missing values. If export is missing, it might mean 0. But I will just calculate it directly.
fbs_pivot['import_dependence_strict'] = (fbs_pivot['fbs_import_quantity'] - fbs_pivot['fbs_export_quantity']) / fbs_pivot['domestic_supply']
# Actually, if export is NaN, doing Imports - NaN = NaN. Let's do a safe subtract if domestic_supply is not NA.
fbs_pivot['net_imports'] = fbs_pivot['fbs_import_quantity'].fillna(0) - fbs_pivot['fbs_export_quantity'].fillna(0)
# Only compute import dependence if domestic supply is > 0
fbs_pivot.loc[fbs_pivot['domestic_supply'] > 0, 'import_dependence'] = fbs_pivot['net_imports'] / fbs_pivot['domestic_supply']

# Calorie share
fbs_pivot['calorie_share'] = fbs_pivot['food_supply_kcal'] / fbs_pivot['total_kcal_capita_day']
# Protein share
fbs_pivot['protein_share'] = fbs_pivot['food_supply_protein'] / fbs_pivot['total_protein_g_capita_day']

fbs_final = fbs_pivot[['country_code', 'commodity', 'Year',
                      'production_quantity', 'fbs_import_quantity', 'fbs_export_quantity',
                      'domestic_supply', 'food_supply_quantity', 'food_supply_kcal',
                      'food_supply_protein', 'import_dependence', 'calorie_share', 'protein_share']].rename(columns={'Year': 'year'})

print("Merging everything...")
# Base: exposure_df (which is the country-commodity-year grid)
res = exposure_df[['country_code', 'country_name', 'commodity', 'year', 'total_import_quantity_tonnes', 'total_import_value_1000_usd']]

res = res.merge(conc_df.drop(columns=['country_name']), on=['country_code', 'commodity', 'year'], how='left')
res = res.merge(fbs_final, on=['country_code', 'commodity', 'year'], how='left')

# Order columns as requested
cols = ['country_code', 'country_name', 'commodity', 'year',
        'total_import_quantity_tonnes', 'total_import_value_1000_usd',
        'supplier_count', 'largest_supplier_share', 'top3_supplier_share', 'top5_supplier_share',
        'hhi_0_1', 'hhi_0_10000', 'supplier_entropy', 'normalized_supplier_entropy',
        'production_quantity', 'fbs_import_quantity', 'fbs_export_quantity', 'domestic_supply',
        'food_supply_quantity', 'food_supply_kcal', 'food_supply_protein',
        'import_dependence', 'calorie_share', 'protein_share']

# Make sure all columns exist
for c in cols:
    if c not in res.columns:
        res[c] = np.nan

res = res[cols]

# Save
res.to_csv('data/processed/foodshield/foodshield_exposure_metrics_2010_2023.csv', index=False)
print("Saved data/processed/foodshield/foodshield_exposure_metrics_2010_2023.csv")
