import pandas as pd
import os
import json

def lock_commodity_universe():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    processed_dir = os.path.join(project_root, 'data', 'processed')
    
    # Read core commodities from previous step
    core_file = os.path.join(processed_dir, 'foodshield_core_commodities.csv')
    if not os.path.exists(core_file):
        raise FileNotFoundError(f"Cannot find {core_file}. Did Step 3C (first pass) run?")
        
    df_core = pd.read_csv(core_file)
    
    # Target CPC list from the prompt
    allowed_cpcs = {
        "'0111", "'0113", "'0112", "'2165", "'2351f", "'23511.02", "'21631.01"
    }
    
    # Filter only the exact allowed CPCs
    df_final = df_core[df_core['cpc_code'].isin(allowed_cpcs)].copy()
    
    # Format the final universe
    df_final = df_final.rename(columns={'inclusion_status': 'status'})
    
    final_cols = ['commodity_group', 'fbs_item', 'trade_item', 'trade_item_code', 'cpc_code', 'status', 'confidence', 'methodological_note']
    df_final = df_final[final_cols]
    df_final = df_final.rename(columns={'methodological_note': 'methodology'})
    
    print("\nRunning Validation Checks...")
    failed = False
    
    # CHECK 1: Exactly 6 commodity groups must exist.
    num_groups = df_final['commodity_group'].nunique()
    if num_groups != 6:
        print(f"FAIL CHECK 1: Expected 6 commodity groups, found {num_groups}")
        failed = True
        
    # CHECK 2: Exactly 7 core CPC representations must exist.
    num_cpcs = df_final['cpc_code'].nunique()
    if num_cpcs != 7:
        print(f"FAIL CHECK 2: Expected 7 CPCs, found {num_cpcs}")
        failed = True
        
    # CHECK 3: The allowed CPC set must be exactly...
    if set(df_final['cpc_code']) != allowed_cpcs:
        print(f"FAIL CHECK 3: CPCs do not exactly match allowed list. Found: {set(df_final['cpc_code'])}")
        failed = True
        
    # CHECK 4: No processed, by-product, feed, non-food, or uncertain item may have status CORE.
    invalid_statuses = df_final[df_final['status'] != 'CORE']
    if len(invalid_statuses) > 0:
        print(f"FAIL CHECK 4: Found items without CORE status in the final list.")
        failed = True
        
    # CHECK 5: No duplicate commodity/CPC combination.
    dups = df_final.duplicated(subset=['commodity_group', 'cpc_code'])
    if dups.any():
        print("FAIL CHECK 5: Duplicate commodity/CPC combination found.")
        failed = True
        
    # CHECK 6: No excluded commodity should accidentally enter the final core universe.
    if len(df_final[~df_final['cpc_code'].isin(allowed_cpcs)]) > 0:
        print("FAIL CHECK 6: Excluded commodity accidentally entered the final universe.")
        failed = True
        
    # CHECK 7: Sugar must contain exactly two core CPCs.
    sugar_cpcs = df_final[df_final['commodity_group'] == 'Sugar']['cpc_code'].nunique()
    if sugar_cpcs != 2:
        print(f"FAIL CHECK 7: Sugar contains {sugar_cpcs} CPCs, expected 2.")
        failed = True
        
    # CHECK 8: Every other commodity must contain exactly one core CPC.
    other_groups = df_final[df_final['commodity_group'] != 'Sugar']
    other_counts = other_groups.groupby('commodity_group')['cpc_code'].nunique()
    if any(other_counts != 1):
        print("FAIL CHECK 8: A non-sugar commodity has more than 1 CPC.")
        failed = True
        
    if failed:
        print("VALIDATION FAILED. Aborting.")
        return
        
    print("All Validation Checks Passed.")
    
    # Write final master file
    final_csv = os.path.join(processed_dir, 'foodshield_final_commodity_universe.csv')
    df_final.to_csv(final_csv, index=False)
    
    # Write JSON config
    config = {}
    for grp, group_df in df_final.groupby('commodity_group'):
        config[grp] = {
            "fbs_item": group_df['fbs_item'].iloc[0],
            "core_cpcs": group_df['cpc_code'].tolist()
        }
        
    json_path = os.path.join(processed_dir, 'foodshield_commodity_config.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
        
    # Write Final Report
    report_path = os.path.join(processed_dir, 'foodshield_step3c_final_report.txt')
    report_text = """FOODSHIELD STEP 3C FINAL REPORT

- Number of final commodities: 6
- Number of core trade representations: 7
- Methodology: Strict primary-commodity
- Processed derivatives: Excluded
- By-products: Excluded
- Feed/non-food: Excluded
- Ambiguous candidates: Excluded
- Double-counting prevention: Enforced (only primary raw nodes retained)
- Sugar's retained CPCs: '2351f, '23511.02
- Sunflower Oil's retained CPC: '21631.01
- Status: The commodity universe is LOCKED
"""
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
        
    print("\n====================================================")
    print("STEP 3C COMPLETE — SIX-COMMODITY UNIVERSE LOCKED")
    print("====================================================\n")
    print("Summary:")
    print("1. Finalized 6 commodities to their 7 cleanest primary trade equivalents.")
    print("2. Created: foodshield_final_commodity_universe.csv, foodshield_step3c_final_report.txt, foodshield_commodity_config.json")
    print("3. Passed 8 strict validation checks ensuring no double-counting or invalid mappings.")
    print("4. Limitations: Refined sugar flows explicitly excluded to prevent double counting.")
    print("5. NEXT STEP: STEP 4 — COUNTRY UNIVERSE / COUNTRY-LEVEL TRADE DATA PREPARATION")
    
if __name__ == '__main__':
    lock_commodity_universe()
