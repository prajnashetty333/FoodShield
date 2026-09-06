import pandas as pd
import numpy as np
from pathlib import Path
import json

def generate_report(stats, val_results, report_path):
    report_content = f"""# FOODSHIELD STEP 8A: SUPPLIER SHOCK ENGINE - VALIDATION REPORT

## 1. Objective
Build a reproducible supplier-disappearance shock engine to simulate the immediate supply loss if a foreign supplier disappears, using the historical bilateral supplier network.

## 2. Methodology
The historical bilateral trade network was aggregated by Importer × Commodity × Year × Supplier. Self-trade was excluded. Suppliers were ranked by descending import quantity (with supplier country code as deterministic tie-breaker).

## 3. Shock Definition
For every supplier, we simulate their disappearance:
- `baseline_imports(C,F,Y)` = sum of all positive supplier import quantities
- `lost_supply(C,F,Y,S)` = `import_quantity(C,S,F,Y)`
- `shocked_imports(C,F,Y,S)` = `baseline_imports(C,F,Y)` - `lost_supply(C,F,Y,S)`
- `shock_loss_share(C,F,Y,S)` = `lost_supply` / `baseline_imports`
- `remaining_import_share` = 1 - `shock_loss_share`

## 4. Mathematical Formulas
See above Section 3.

## 5. Input Datasets
- `data/processed/foodshield/foodshield_bilateral_trade_2010_2023.csv`
- `data/processed/foodshield/foodshield_exposure_metrics_2010_2023.csv`

## 6. Number of importer-commodity-year observations
{stats['num_icy']}

## 7. Number of supplier shock observations
{stats['num_shocks']}

## 8. Number of Rank 1 scenarios
{stats['num_rank_1']}

## 9. Number of Rank 2 scenarios
{stats['num_rank_2']}

## 10. Number of Rank 3 scenarios
{stats['num_rank_3']}

## 11. Number of single-supplier cases
{stats['num_single_supplier']}

## 12. Number of two-supplier cases
{stats['num_two_supplier']}

## 13. Average Rank 1 shock loss
{stats['avg_rank1_loss']:.4f}

## 14. Median Rank 1 shock loss
{stats['median_rank1_loss']:.4f}

## 15. Maximum Rank 1 shock loss
{stats['max_rank1_loss']:.4f}

## 16. Commodity-level shock statistics
Average Rank 1 shock loss by commodity:
{stats['comm_stats']}

## 17. Country-level shock statistics
Overall shock statistics summarized in outputs. Average Rank 1 loss across all countries is {stats['avg_rank1_loss']:.4f}.

## 18. Validation Results
"""
    
    all_passed = True
    for check_name, status in val_results.items():
        pass_str = "PASS" if status else "FAIL"
        report_content += f"- {check_name}: {pass_str}\n"
        if not status:
            all_passed = False
            
    final_status = "PASS" if all_passed else "FAIL"
            
    report_content += f"""
## 19. Edge Cases
- Single-supplier cases mapped to rank 1, shock loss 1.0, remaining 0.
- Missing values for quantity were ignored (only positive flows used).
- Self-trade was excluded.
- Sugar representations aggregated.

## 20. Limitations
- Values assume no immediate substitution or replacement supply (to be addressed in Step 8B).
- Missing quantities are not imputed.

## 21. Methodological Decisions
- Quantity is the primary shock measure.
- Supplier code used as deterministic tie-breaker for ranks.

## 22. Final PASS/FAIL status
{final_status}

### WHAT WE DID
- Ingested bilateral trade data and locked exposure metrics.
- Excluded self-trade and filtered to positive quantities.
- Aggregated duplicate commodity representations (Sugar).
- Ranked suppliers by quantity and computed shock metrics (Rank 1, 2, 3, etc.).
- Generated detailed shock dataset, standard scenarios, and summary tables.
- Validated inputs and logic with 15 rigorous checks.

### WHAT WE DO NEXT
- Explain that STEP 8B will build the Replacement Engine.
"""
    with open(report_path, "w") as f:
        f.write(report_content)
    
    return all_passed


def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    data_dir = root_dir / 'data' / 'processed' / 'foodshield'
    out_dir = data_dir
    report_dir = root_dir / 'reports' / 'validation'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Datasets
    print("Loading data...")
    df_bilateral = pd.read_csv(data_dir / 'foodshield_bilateral_trade_2010_2023.csv')
    df_metrics = pd.read_csv(data_dir / 'foodshield_exposure_metrics_2010_2023.csv')
    
    # 2. Filter Rules
    print("Filtering and aggregating data...")
    LOCKED_COMMODITIES = ['Wheat', 'Rice', 'Maize', 'Palm Oil', 'Sugar', 'Sunflower Oil']
    df = df_bilateral[df_bilateral['commodity'].isin(LOCKED_COMMODITIES)].copy()
    df = df[df['import_quantity_tonnes'] > 0]
    df = df[df['reporter_country_code'] != df['partner_country_code']]
    
    # Check if value column exists
    has_value = 'import_value_1000_usd' in df.columns
    
    # Aggregate (Handle Sugar duplicates and any other potential duplicates)
    agg_dict = {'import_quantity_tonnes': 'sum'}
    if has_value:
        agg_dict['import_value_1000_usd'] = 'sum'
        
    df_agg = df.groupby(['reporter_country_code', 'reporter_country_name', 'commodity', 'year', 'partner_country_code', 'partner_country_name'], as_index=False).agg(agg_dict)
    
    # Rename partner to supplier
    df_agg.rename(columns={
        'reporter_country_code': 'importer_country_code',
        'reporter_country_name': 'importer_country_name',
        'partner_country_code': 'supplier_country_code',
        'partner_country_name': 'supplier_country_name'
    }, inplace=True)
    
    # Calculate baseline imports
    print("Calculating metrics...")
    df_baseline = df_agg.groupby(['importer_country_code', 'commodity', 'year'], as_index=False).agg(
        baseline_import_quantity_tonnes=('import_quantity_tonnes', 'sum'),
        baseline_supplier_count=('supplier_country_code', 'count')
    )
    if has_value:
        df_baseline_val = df_agg.groupby(['importer_country_code', 'commodity', 'year'], as_index=False).agg(
            baseline_import_value_1000_usd=('import_value_1000_usd', 'sum')
        )
        df_baseline = df_baseline.merge(df_baseline_val, on=['importer_country_code', 'commodity', 'year'])
    
    df_shock = df_agg.merge(df_baseline, on=['importer_country_code', 'commodity', 'year'])
    
    # Ranking
    df_shock.sort_values(by=['importer_country_code', 'commodity', 'year', 'import_quantity_tonnes', 'supplier_country_code'], 
                         ascending=[True, True, True, False, True], inplace=True)
    df_shock['supplier_rank'] = df_shock.groupby(['importer_country_code', 'commodity', 'year']).cumcount() + 1
    
    # Calculate shock loss
    df_shock['lost_supply_quantity_tonnes'] = df_shock['import_quantity_tonnes']
    df_shock['shocked_import_quantity_tonnes'] = df_shock['baseline_import_quantity_tonnes'] - df_shock['lost_supply_quantity_tonnes']
    df_shock['shock_loss_share'] = df_shock['lost_supply_quantity_tonnes'] / df_shock['baseline_import_quantity_tonnes']
    df_shock['remaining_import_share'] = 1 - df_shock['shock_loss_share']
    
    # Retain variables
    df_shock['supplier_share'] = df_shock['shock_loss_share']
    df_shock['shock_scenario'] = "Rank " + df_shock['supplier_rank'].astype(str) + " Supplier Disappearance"
    df_shock['shock_severity_raw'] = df_shock['shock_loss_share']
    
    if has_value:
        df_shock['lost_supply_value_1000_usd'] = df_shock['import_value_1000_usd']
        df_shock['shocked_import_value_1000_usd'] = df_shock['baseline_import_value_1000_usd'] - df_shock['lost_supply_value_1000_usd']
        df_shock['shock_loss_value_share'] = np.where(df_shock['baseline_import_value_1000_usd'] > 0, df_shock['lost_supply_value_1000_usd'] / df_shock['baseline_import_value_1000_usd'], 0)

    # Scenarios dataset
    df_scenarios = df_shock[df_shock['supplier_rank'].isin([1, 2, 3])].copy()
    
    # Summary dataset
    # Pivot rank losses
    df_summary = df_baseline.copy()
    for rank in [1, 2, 3]:
        rank_data = df_scenarios[df_scenarios['supplier_rank'] == rank][['importer_country_code', 'commodity', 'year', 'shock_loss_share', 'remaining_import_share']]
        rank_data = rank_data.rename(columns={
            'shock_loss_share': f'rank_{rank}_shock_loss',
            'remaining_import_share': f'rank_{rank}_remaining_supply'
        })
        df_summary = df_summary.merge(rank_data, on=['importer_country_code', 'commodity', 'year'], how='left')
    
    print("Running validation tests...")
    val_results = {}
    # CHECK 1
    ch1_test = df_shock.groupby(['importer_country_code', 'commodity', 'year'])['lost_supply_quantity_tonnes'].sum().reset_index()
    ch1_base = df_baseline[['importer_country_code', 'commodity', 'year', 'baseline_import_quantity_tonnes']]
    ch1_merge = ch1_test.merge(ch1_base, on=['importer_country_code', 'commodity', 'year'])
    val_results['CHECK 1: sum supplier quantities = baseline imports'] = np.allclose(ch1_merge['lost_supply_quantity_tonnes'], ch1_merge['baseline_import_quantity_tonnes'])

    # CHECK 2
    ch2_test = df_shock.groupby(['importer_country_code', 'commodity', 'year'])['supplier_share'].sum().reset_index()
    val_results['CHECK 2: Supplier shares sum to ~1'] = np.allclose(ch2_test['supplier_share'], 1.0)
    
    # CHECK 3
    val_results['CHECK 3: shocked_imports = baseline - lost_supply'] = np.allclose(df_shock['shocked_import_quantity_tonnes'], df_shock['baseline_import_quantity_tonnes'] - df_shock['lost_supply_quantity_tonnes'])
    
    # CHECK 4
    val_results['CHECK 4: remaining_import_share = 1 - shock_loss_share'] = np.allclose(df_shock['remaining_import_share'], 1 - df_shock['shock_loss_share'])
    
    # CHECK 5
    rank1 = df_shock[df_shock['supplier_rank'] == 1]
    max_qty = df_shock.groupby(['importer_country_code', 'commodity', 'year'])['lost_supply_quantity_tonnes'].max().reset_index()
    ch5_merge = rank1.merge(max_qty, on=['importer_country_code', 'commodity', 'year'], suffixes=('', '_max'))
    val_results['CHECK 5: Rank 1 equals largest supplier by quantity'] = np.allclose(ch5_merge['lost_supply_quantity_tonnes'], ch5_merge['lost_supply_quantity_tonnes_max'])
    
    # CHECK 6
    rank2 = df_shock[df_shock['supplier_rank'] == 2][['importer_country_code', 'commodity', 'year', 'lost_supply_quantity_tonnes']]
    ch6_merge = rank1.merge(rank2, on=['importer_country_code', 'commodity', 'year'], suffixes=('_1', '_2'))
    val_results['CHECK 6: Rank 2 quantity <= Rank 1 quantity'] = all(ch6_merge['lost_supply_quantity_tonnes_2'] <= ch6_merge['lost_supply_quantity_tonnes_1'] + 1e-9)

    # CHECK 7
    rank3 = df_shock[df_shock['supplier_rank'] == 3][['importer_country_code', 'commodity', 'year', 'lost_supply_quantity_tonnes']]
    ch7_merge = rank2.merge(rank3, on=['importer_country_code', 'commodity', 'year'], suffixes=('_2', '_3'))
    val_results['CHECK 7: Rank 3 quantity <= Rank 2 quantity'] = all(ch7_merge['lost_supply_quantity_tonnes_3'] <= ch7_merge['lost_supply_quantity_tonnes_2'] + 1e-9)
    
    # CHECK 8
    val_results['CHECK 8: shock_loss_share between 0 and 1'] = (df_shock['shock_loss_share'] >= -1e-9).all() and (df_shock['shock_loss_share'] <= 1.0 + 1e-9).all()
    
    # CHECK 9
    val_results['CHECK 9: remaining_import_share between 0 and 1'] = (df_shock['remaining_import_share'] >= -1e-9).all() and (df_shock['remaining_import_share'] <= 1.0 + 1e-9).all()
    
    # CHECK 10
    val_results['CHECK 10: No self-trade edges'] = len(df_shock[df_shock['importer_country_code'] == df_shock['supplier_country_code']]) == 0
    
    # CHECK 11
    val_results['CHECK 11: Only locked commodities appear'] = set(df_shock['commodity'].unique()).issubset(set(LOCKED_COMMODITIES))
    
    # CHECK 12
    val_results['CHECK 12: Years 2010-2023'] = df_shock['year'].min() >= 2010 and df_shock['year'].max() <= 2023
    
    # CHECK 13
    val_results['CHECK 13: No duplicate analytical keys'] = not df_shock.duplicated(subset=['importer_country_code', 'supplier_country_code', 'commodity', 'year']).any()
    
    # CHECK 14
    df_metrics = df_metrics.rename(columns={'country_code': 'importer_country_code'})
    ch14_merge = rank1.merge(df_metrics[['importer_country_code', 'commodity', 'year', 'largest_supplier_share']], on=['importer_country_code', 'commodity', 'year'], how='inner')
    val_results['CHECK 14: Rank 1 share equals STEP 7A largest_supplier_share'] = np.allclose(ch14_merge['shock_loss_share'], ch14_merge['largest_supplier_share'])
    
    # CHECK 15
    ch15_merge = df_baseline.merge(df_metrics[['importer_country_code', 'commodity', 'year', 'total_import_quantity_tonnes']], on=['importer_country_code', 'commodity', 'year'], how='inner')
    # Use a tolerance for float differences
    ch15_pass = np.allclose(ch15_merge['baseline_import_quantity_tonnes'], ch15_merge['total_import_quantity_tonnes'], equal_nan=True)
    val_results['CHECK 15: Reconcile baseline imports with STEP 7'] = ch15_pass
    if not ch15_pass:
        diffs = ch15_merge[~np.isclose(ch15_merge['baseline_import_quantity_tonnes'], ch15_merge['total_import_quantity_tonnes'])]
        print("WARNING: Check 15 discrepancy found! First few differences:")
        print(diffs.head())
    
    # Compute Stats
    stats = {
        'num_icy': len(df_baseline),
        'num_shocks': len(df_shock),
        'num_rank_1': len(rank1),
        'num_rank_2': len(df_shock[df_shock['supplier_rank'] == 2]),
        'num_rank_3': len(df_shock[df_shock['supplier_rank'] == 3]),
        'num_single_supplier': len(df_baseline[df_baseline['baseline_supplier_count'] == 1]),
        'num_two_supplier': len(df_baseline[df_baseline['baseline_supplier_count'] == 2]),
        'avg_rank1_loss': rank1['shock_loss_share'].mean(),
        'median_rank1_loss': rank1['shock_loss_share'].median(),
        'max_rank1_loss': rank1['shock_loss_share'].max(),
        'comm_stats': rank1.groupby('commodity')['shock_loss_share'].mean().to_dict()
    }
    
    # Ensure ordered columns
    cols = [
        'year', 'importer_country_code', 'importer_country_name',
        'supplier_country_code', 'supplier_country_name', 'commodity',
        'supplier_rank', 'baseline_import_quantity_tonnes', 'lost_supply_quantity_tonnes',
        'shocked_import_quantity_tonnes', 'shock_loss_share', 'remaining_import_share',
        'supplier_share', 'baseline_supplier_count', 'shock_scenario', 'shock_severity_raw'
    ]
    if has_value:
        cols += ['baseline_import_value_1000_usd', 'lost_supply_value_1000_usd', 'shocked_import_value_1000_usd', 'shock_loss_value_share']
    
    df_shock = df_shock[[c for c in cols if c in df_shock.columns]]
    
    print("Saving outputs...")
    df_shock.to_csv(out_dir / 'foodshield_supplier_shock_2010_2023.csv', index=False)
    df_scenarios.to_csv(out_dir / 'foodshield_shock_scenarios_2010_2023.csv', index=False)
    df_summary.to_csv(out_dir / 'foodshield_shock_summary_2010_2023.csv', index=False)
    
    print("Generating report...")
    report_path = report_dir / 'FOODSHIELD_STEP_8A_SUPPLIER_SHOCK_VALIDATION_REPORT.md'
    all_passed = generate_report(stats, val_results, report_path)
    
    for k, v in val_results.items():
        print(f"{k}: {'PASS' if v else 'FAIL'}")
        
    print(f"\nFinal Validation Status: {'PASS' if all_passed else 'FAIL'}")

if __name__ == '__main__':
    main()
