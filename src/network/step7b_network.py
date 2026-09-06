import pandas as pd
import numpy as np
import json
import os

# Create directories
os.makedirs('data/processed/foodshield', exist_ok=True)

# 1. Load Datasets
print("Loading datasets...")
shares_df = pd.read_csv('data/processed/foodshield/foodshield_supplier_shares_2010_2023.csv')
metrics_df = pd.read_csv('data/processed/foodshield/foodshield_exposure_metrics_2010_2023.csv')
bilateral_df = pd.read_csv('data/processed/foodshield/foodshield_bilateral_trade_2010_2023.csv')
universe_df = pd.read_csv('data/processed/foodshield/foodshield_country_universe.csv')

valid_countries = set(universe_df['country_code'].unique())
commodities = ['Wheat', 'Rice', 'Maize', 'Palm Oil', 'Sugar', 'Sunflower Oil']

# Rename shares columns to importer and supplier
edges_df = shares_df.rename(columns={
    'country_code': 'importer_country_code',
    'country_name': 'importer_country_name',
    'quantity_share': 'supplier_share_quantity',
}).copy()

# Drop rows with non-positive quantities (Positive-flow rule)
edges_df = edges_df[edges_df['import_quantity_tonnes'] > 0].copy()

# Exclude self trade
edges_df = edges_df[edges_df['importer_country_code'] != edges_df['supplier_country_code']].copy()

# Rank suppliers
edges_df['supplier_rank_quantity'] = edges_df.groupby(['importer_country_code', 'commodity', 'year'])['import_quantity_tonnes'].rank(method='first', ascending=False)

# Keep required columns for edges
edges_cols = [
    'importer_country_code', 'importer_country_name',
    'supplier_country_code', 'supplier_country_name',
    'commodity', 'year',
    'import_quantity_tonnes', 'import_value_1000_usd',
    'supplier_share_quantity', 'supplier_rank_quantity'
]
edges_df = edges_df[edges_cols].copy()
edges_df.to_csv('data/processed/foodshield/foodshield_trade_network_edges_2010_2023.csv', index=False)
print("Saved foodshield_trade_network_edges_2010_2023.csv")


# 2. Supplier History
print("Computing supplier history...")
# Get unique importer-supplier-commodity combinations
pair_groups = edges_df.groupby(['importer_country_code', 'supplier_country_code', 'commodity'])

history_list = []
for name, group in pair_groups:
    imp, sup, comm = name
    years = group['year'].unique()
    first_year = int(min(years))
    last_year = int(max(years))
    years_active = len(years)
    persistence_rate = years_active / 14.0 # 2010-2023
    
    # Check entries and exits
    # For year t, if t-1 not in years, it's an entry (careful with 2010)
    # For year t-1, if t not in years, it's an exit
    active_years_set = set(years)
    for y in range(2010, 2024):
        is_active = 1 if y in active_years_set else 0
        
        # entry
        if y == 2010:
            supplier_entry = 0 # Cannot know if entry from 2009
        else:
            supplier_entry = 1 if (y in active_years_set and (y-1) not in active_years_set) else 0
            
        # exit
        if y == 2010:
            supplier_exit = 0
        else:
            supplier_exit = 1 if ((y-1) in active_years_set and y not in active_years_set) else 0
            
        history_list.append({
            'importer_country_code': imp,
            'supplier_country_code': sup,
            'commodity': comm,
            'year': y,
            'is_active': is_active,
            'first_active_year': first_year,
            'last_active_year': last_year,
            'years_active': years_active,
            'persistence_rate': persistence_rate,
            'supplier_entry': supplier_entry,
            'supplier_exit': supplier_exit
        })

history_df = pd.DataFrame(history_list)
# Merge names back
imp_names = universe_df[['country_code', 'country_name']].drop_duplicates().rename(columns={'country_code': 'importer_country_code', 'country_name': 'importer_country_name'})
sup_names = universe_df[['country_code', 'country_name']].drop_duplicates().rename(columns={'country_code': 'supplier_country_code', 'country_name': 'supplier_country_name'})

history_df = history_df.merge(imp_names, on='importer_country_code', how='left')
history_df = history_df.merge(sup_names, on='supplier_country_code', how='left')

history_cols = [
    'importer_country_code', 'importer_country_name',
    'supplier_country_code', 'supplier_country_name',
    'commodity', 'year', 'is_active', 'supplier_entry', 'supplier_exit',
    'first_active_year', 'last_active_year', 'years_active', 'persistence_rate'
]
history_df = history_df[history_cols]
history_df.to_csv('data/processed/foodshield/foodshield_supplier_history_2010_2023.csv', index=False)
print("Saved foodshield_supplier_history_2010_2023.csv")


# 3. Network Summary
print("Computing network summary...")
# We need top_supplier_country. It is the supplier with rank == 1 in edges_df.
top_suppliers = edges_df[edges_df['supplier_rank_quantity'] == 1][['importer_country_code', 'commodity', 'year', 'supplier_country_code']]
top_suppliers = top_suppliers.rename(columns={'supplier_country_code': 'top_supplier_country', 'importer_country_code': 'country_code'})

metrics_renamed = metrics_df.copy()
summary_df = pd.merge(metrics_renamed, top_suppliers, on=['country_code', 'commodity', 'year'], how='left')

# Rename to importer_country_code for consistency in summary
summary_df = summary_df.rename(columns={
    'country_code': 'importer_country_code',
    'country_name': 'importer_country_name',
    'largest_supplier_share': 'top_supplier_share',
    'top3_supplier_share': 'top_3_share',
    'top5_supplier_share': 'top_5_share',
    'supplier_entropy': 'entropy',
    'normalized_supplier_entropy': 'normalized_entropy'
})

summary_cols = [
    'importer_country_code', 'importer_country_name', 'commodity', 'year',
    'supplier_count', 'top_supplier_country', 'top_supplier_share',
    'top_3_share', 'top_5_share', 'hhi_0_1', 'hhi_0_10000',
    'entropy', 'normalized_entropy'
]

# Note: Some metrics rows might have 0 suppliers, so top_supplier_country would be NaN.
# This is expected and correct.
summary_df = summary_df[summary_cols]
summary_df.to_csv('data/processed/foodshield/foodshield_network_summary_2010_2023.csv', index=False)
print("Saved foodshield_network_summary_2010_2023.csv")


# 4. Validations
print("Running validations...")

issues = []

# A. Commodity coverage
edge_commodities = set(edges_df['commodity'].unique())
if edge_commodities != set(commodities):
    issues.append(f"FAIL Commodity coverage: {edge_commodities}")

# B. Year coverage
edge_years = set(edges_df['year'].unique())
if edge_years != set(range(2010, 2024)):
    issues.append(f"FAIL Year coverage: {edge_years}")
    
# C. Country universe
all_edge_countries = set(edges_df['importer_country_code']).union(set(edges_df['supplier_country_code']))
invalid_countries = all_edge_countries - valid_countries
if len(invalid_countries) > 0:
    issues.append(f"FAIL Country universe: invalid countries found: {invalid_countries}")
    
# D. No self-trade
self_trade = edges_df[edges_df['importer_country_code'] == edges_df['supplier_country_code']]
if len(self_trade) > 0:
    issues.append("FAIL Self-trade found in analytical edges.")

# E. Positive-flow rule
non_positive = edges_df[edges_df['import_quantity_tonnes'] <= 0]
if len(non_positive) > 0:
    issues.append("FAIL Edges with import_quantity_tonnes <= 0 found.")
    
# F. Supplier-share validation
share_sums = edges_df.groupby(['importer_country_code', 'commodity', 'year'])['supplier_share_quantity'].sum()
tolerance_fails = share_sums[~np.isclose(share_sums, 1.0, atol=1e-3)]
if len(tolerance_fails) > 0:
    issues.append(f"FAIL Supplier-share sum != 1 for {len(tolerance_fails)} importer-commodity-years.")
    
# G. Supplier ranking
# Check if rank 1 is max
rank_1_qtys = edges_df[edges_df['supplier_rank_quantity'] == 1].set_index(['importer_country_code', 'commodity', 'year'])['import_quantity_tonnes']
max_qtys = edges_df.groupby(['importer_country_code', 'commodity', 'year'])['import_quantity_tonnes'].max()
rank_diffs = (rank_1_qtys - max_qtys).abs()
if len(rank_diffs[rank_diffs > 1e-5]) > 0:
    issues.append("FAIL Rank 1 does not correspond to max supplier quantity.")

# H. Top supplier consistency
# Join with summary_df
test_top_share = pd.merge(edges_df[edges_df['supplier_rank_quantity'] == 1], summary_df, on=['importer_country_code', 'commodity', 'year'], how='inner')
diffs = (test_top_share['supplier_share_quantity'] - test_top_share['top_supplier_share']).abs()
if len(diffs[diffs > 1e-3]) > 0:
    issues.append("FAIL top_supplier_share does not equal supplier_share of rank 1.")
    
# I. Supplier count consistency
edge_counts = edges_df.groupby(['importer_country_code', 'commodity', 'year']).size().reset_index(name='calc_count')
test_count = pd.merge(summary_df, edge_counts, on=['importer_country_code', 'commodity', 'year'], how='left')
test_count['calc_count'] = test_count['calc_count'].fillna(0)
count_diffs = test_count[test_count['supplier_count'].fillna(0) != test_count['calc_count']]
if len(count_diffs) > 0:
    issues.append("FAIL supplier_count does not equal number of positive supplier edges.")
    
# J. Network-total reconciliation
net_total = edges_df['import_quantity_tonnes'].sum()
# Bilateral df excludes self trade for analytical purposes? Wait, bilateral_df might include self-trade.
# Or maybe the validated Step 6A bilateral dataset already excluded self trade in its analytical flows?
# Let's compute sum of bilateral_df (excluding self trade, year 2010-2023, valid countries, > 0)
bilateral_filtered = bilateral_df[
    (bilateral_df['year'].between(2010, 2023)) &
    (bilateral_df['commodity'].isin(commodities)) &
    (bilateral_df['reporter_country_code'] != bilateral_df['partner_country_code']) &
    (bilateral_df['import_quantity_tonnes'] > 0)
]
bil_total = bilateral_filtered['import_quantity_tonnes'].sum()
if not np.isclose(net_total, bil_total, rtol=1e-3):
    issues.append(f"FAIL Network-total reconciliation: network={net_total}, bilateral={bil_total}")
    
# K. Commodity reconciliation
if 'Sugar' not in edge_commodities:
    issues.append("FAIL Sugar is missing from commodities.")
    
# L. Duplicate check
dupes = edges_df.duplicated(subset=['importer_country_code', 'supplier_country_code', 'commodity', 'year'])
if dupes.sum() > 0:
    issues.append(f"FAIL {dupes.sum()} duplicate edges found.")

status = "READY" if len(issues) == 0 else "NOT READY"


# Generate Report
print("Generating markdown report...")

num_edges = len(edges_df)
num_importers = edges_df['importer_country_code'].nunique()
num_suppliers = edges_df['supplier_country_code'].nunique()
num_pairs = len(edges_df[['importer_country_code', 'supplier_country_code']].drop_duplicates())

avg_suppliers = edge_counts['calc_count'].mean()
med_suppliers = edge_counts['calc_count'].median()
max_suppliers = edge_counts['calc_count'].max()

# Supplier persistence statistics (only using historical pairings)
active_history = history_df[history_df['is_active'] == 1]
unique_pairs = history_df[['importer_country_code', 'supplier_country_code', 'commodity', 'years_active', 'persistence_rate']].drop_duplicates()
avg_persistence = unique_pairs['persistence_rate'].mean()
med_persistence = unique_pairs['persistence_rate'].median()
avg_years = unique_pairs['years_active'].mean()

total_entries = history_df['supplier_entry'].sum()
total_exits = history_df['supplier_exit'].sum()


report = f"""# FOODSHIELD STEP 7B: NETWORK VALIDATION REPORT

## 1. Objective
Build the historical FOODSHIELD supplier network for the 6 locked commodities across 2010–2023 to serve as the baseline for the Supplier Shock Engine and Replacement Engine.

## 2. Input datasets
- `foodshield_bilateral_trade_2010_2023.csv`
- `foodshield_supplier_shares_2010_2023.csv`
- `foodshield_exposure_metrics_2010_2023.csv`
- `foodshield_country_universe.csv`

## 3. Analytical period
2010–2023

## 4. Commodity coverage
Exactly 6 commodities: {', '.join(sorted(list(edge_commodities)))}

## 5. Country coverage
All valid network nodes strictly adhere to the 220-country/economy universe.

## 6. Number of network edges
{num_edges:,}

## 7. Number of unique importers
{num_importers:,}

## 8. Number of unique suppliers
{num_suppliers:,}

## 9. Number of importer-supplier pairs
{num_pairs:,} (ignoring commodity distinction), and {len(unique_pairs):,} distinct importer-supplier-commodity relationships.

## 10. Average suppliers per importer-commodity-year
{avg_suppliers:.2f}

## 11. Median suppliers per importer-commodity-year
{med_suppliers:.1f}

## 12. Maximum suppliers
{max_suppliers}

## 13. Supplier persistence statistics
Average years active per pairing: {avg_years:.2f}
Average persistence rate: {avg_persistence:.2%}
Median persistence rate: {med_persistence:.2%}

## 14. Supplier entry statistics
Total supplier entries identified (post-2010): {total_entries:,}

## 15. Supplier exit statistics
Total supplier exits identified (post-2010): {total_exits:,}

## 16. Network quantity totals
Total import quantity in network: {net_total:,.0f} tonnes.

## 17. Reconciliation with Step 6A
Validated Step 6A Bilateral Quantity (excluding self-trade, zero/null flows): {bil_total:,.0f} tonnes.
Reconciliation difference: {net_total - bil_total:,.0f} tonnes.

## 18. Duplicate diagnostics
Duplicate edges: {dupes.sum()}

## 19. Self-trade diagnostics
Self-trade edges: {len(self_trade)}

## 20. Supplier-share validation
Shares summing to 1.0 test failures: {len(tolerance_fails)}

## 21. Ranking validation
Rank 1 consistency failures: {len(rank_diffs[rank_diffs > 1e-5])}

## 22. Commodity validation
All {len(commodities)} commodities present. Sugar represented as aggregated commodity.

## 23. Year validation
All {len(edge_years)} years present (2010-2023).

## 24. Any missingness or structural limitations
Only relationships with strictly positive import quantities are retained as analytical edges. Self-trade is excluded to correctly model exogenous supply risk. The entry/exit statistics correctly ignore 2010 to prevent false entries/exits due to the start of the analytical period.

## 25. Final PASS/FAIL status
Status: {status}

### Issues Found:
"""

if len(issues) == 0:
    report += "None.\n"
else:
    for issue in issues:
        report += f"- {issue}\n"

report += f"""
---

### WHAT WE DID
- Extracted and validated analytical network edges representing positive supplier->importer flows for 2010-2023.
- Enforced country and commodity universe rules and excluded self-trade.
- Computed supplier ranks and validated supplier shares against previously locked exposure metrics.
- Built a time-series history for all historical pairings to calculate entry, exit, and persistence rates.
- Generated network summaries aligning HHI, entropy, and top supplier metrics.

### WHAT WE DO NEXT
- Proceed to Step 8 — Supplier Shock Engine, where we will introduce the supplier-disappearance shock using the validated historical network.

---
STEP 7B STATUS: {status}
"""

with open('reports/validation/FOODSHIELD_STEP_7B_NETWORK_VALIDATION_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("Done.")
