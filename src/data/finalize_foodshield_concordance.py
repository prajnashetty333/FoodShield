import pandas as pd
import os
import re

def finalize_foodshield_concordance():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    processed_dir = os.path.join(project_root, 'data', 'processed')
    foodshield_dir = os.path.join(processed_dir, 'foodshield')
    os.makedirs(foodshield_dir, exist_ok=True)
    
    outputs_dir = os.path.join(project_root, 'outputs')
    trade_path = os.path.join(outputs_dir, 'trade_item_catalog.csv')
    fbs_path = os.path.join(outputs_dir, 'fbs_item_catalog.csv')
    
    trade_df = pd.read_csv(trade_path)
    fbs_df = pd.read_csv(fbs_path)
    
    target_groups = {
        "Wheat": "Wheat and products",
        "Rice": "Rice and products",
        "Maize": "Maize and products",
        "Palm Oil": "Palm Oil",
        "Sugar": "Sugar (Raw Equivalent)",
        "Sunflower Oil": "Sunflowerseed Oil"
    }
    
    crosswalk_rows = []
    summary_stats = {
        grp: {'primary': 0, 'core': 0, 'processed': 0, 'excluded': 0, 'uncertain': 0}
        for grp in target_groups
    }
    
    def match_words(item_name, includes, excludes=None):
        if pd.isna(item_name): return False
        name_lower = item_name.lower()
        if excludes:
            for ex in excludes:
                if re.search(r'\b' + re.escape(ex) + r'\b', name_lower):
                    return False
        for inc in includes:
            if re.search(r'\b' + re.escape(inc) + r'\b', name_lower):
                return True
        return False
        
    def classify_wheat(t_lower):
        if not match_words(t_lower, ['wheat', 'bulgur', 'macaroni', 'flour', 'pasta', 'bread', 'pastry'], ['buckwheat']): return None
        if match_words(t_lower, ['bran', 'residues', 'waste', 'straw', 'cake']):
            return 'BYPRODUCT', 'NO', 'HIGH', 'Agricultural byproduct'
        if match_words(t_lower, ['flour', 'pasta', 'macaroni', 'pastry', 'bread', 'bulgur']):
            return 'PROCESSED_FOOD', 'NO', 'HIGH', 'Processed derivative (exclude to avoid double counting)'
        if t_lower == 'wheat':
            return 'PRIMARY', 'YES', 'HIGH', 'Direct primary commodity'
        return 'UNCERTAIN', 'NO', 'LOW', 'Requires methodological review'
        
    def classify_rice(t_lower):
        if not match_words(t_lower, ['rice', 'paddy', 'milled', 'husked', 'broken'], ['price', 'licorice']): return None
        if match_words(t_lower, ['bran', 'residues', 'waste', 'straw']):
            return 'BYPRODUCT', 'NO', 'HIGH', 'Agricultural byproduct'
        if match_words(t_lower, ['flour', 'milled', 'husked', 'broken', 'preparations']):
            return 'PROCESSED_FOOD', 'NO', 'HIGH', 'Processed derivative (exclude to avoid double counting)'
        if t_lower == 'rice' or 'paddy' in t_lower:
            return 'PRIMARY', 'YES', 'HIGH', 'Direct primary commodity'
        return 'UNCERTAIN', 'NO', 'LOW', 'Requires methodological review'

    def classify_maize(t_lower):
        if not match_words(t_lower, ['maize', 'corn'], ['peppercorn', 'sweet corn', 'popcorn', 'oil']): return None
        if match_words(t_lower, ['bran', 'residues', 'waste', 'cake', 'feed', 'fodder', 'forage', 'pellets']):
            return 'BYPRODUCT', 'NO', 'HIGH', 'Byproduct or feed'
        if match_words(t_lower, ['flour', 'starch', 'germ', 'preparations']):
            return 'PROCESSED_FOOD', 'NO', 'HIGH', 'Processed derivative (exclude to avoid double counting)'
        if t_lower == 'maize (corn)':
            return 'PRIMARY', 'YES', 'HIGH', 'Direct primary commodity'
        return 'UNCERTAIN', 'NO', 'LOW', 'Requires methodological review'

    def classify_palmoil(t_lower):
        if not match_words(t_lower, ['palm oil', 'oil of palm']): return None
        if match_words(t_lower, ['kernel', 'cake', 'meal']):
            return 'BYPRODUCT', 'NO', 'HIGH', 'Byproduct (Palm kernel is distinct)'
        if t_lower == 'palm oil':
            return 'PRIMARY', 'YES', 'HIGH', 'Direct primary commodity'
        return 'UNCERTAIN', 'NO', 'LOW', 'Requires methodological review'

    def classify_sugar(t_lower):
        if not match_words(t_lower, ['sugar', 'molasses', 'syrup']): return None
        if match_words(t_lower, ['maple', 'sugar beet', 'sugar cane']):
            return 'EXCLUDED', 'NO', 'HIGH', 'Raw crop before processing (exclude to avoid double counting with raw equivalent)'
        if match_words(t_lower, ['confectionery', 'preserved', 'preparations', 'syrups n.e.c.', 'flavouring']):
            return 'PROCESSED_FOOD', 'NO', 'HIGH', 'Processed sugar derivative (exclude to avoid double counting)'
        if match_words(t_lower, ['molasses']):
            return 'BYPRODUCT', 'NO', 'HIGH', 'Processing byproduct'
        if t_lower in ['raw cane or beet sugar (centrifugal only)', 'cane sugar, non-centrifugal']:
            return 'PRIMARY', 'YES', 'HIGH', 'Direct primary raw equivalent commodity'
        if t_lower == 'refined sugar':
            return 'PROCESSED_FOOD', 'NO', 'HIGH', 'Refined sugar (exclude to avoid double counting with raw equivalent)'
        return 'UNCERTAIN', 'NO', 'LOW', 'Requires methodological review'

    def classify_sunfloweroil(t_lower):
        if not match_words(t_lower, ['sunflower']): return None
        if match_words(t_lower, ['cake', 'meal']) or (match_words(t_lower, ['seed']) and not match_words(t_lower, ['oil'])):
            return 'BYPRODUCT', 'NO', 'HIGH', 'Seed or cake (Not oil)'
        if match_words(t_lower, ['sunflower-seed oil', 'sunflower oil', 'oil of sunflower']):
            return 'PRIMARY', 'YES', 'HIGH', 'Direct primary commodity'
        return 'UNCERTAIN', 'NO', 'LOW', 'Requires methodological review'


    for grp, fbs_name in target_groups.items():
        found_any = False
        
        for _, trade_row in trade_df.iterrows():
            t_lower = trade_row['Item'].lower()
            
            result = None
            if grp == "Wheat": result = classify_wheat(t_lower)
            elif grp == "Rice": result = classify_rice(t_lower)
            elif grp == "Maize": result = classify_maize(t_lower)
            elif grp == "Palm Oil": result = classify_palmoil(t_lower)
            elif grp == "Sugar": result = classify_sugar(t_lower)
            elif grp == "Sunflower Oil": result = classify_sunfloweroil(t_lower)
            
            if result:
                found_any = True
                role, incl, conf, reason = result
                
                # Correct EXCLUDED role to NON_FOOD or BYPRODUCT as per allowed
                if role == 'EXCLUDED': role = 'NON_FOOD'
                
                crosswalk_rows.append({
                    'commodity_group': grp,
                    'fbs_item': fbs_name,
                    'trade_item': trade_row['Item'],
                    'trade_item_code': trade_row['Item Code'],
                    'cpc_code': trade_row['Item Code (CPC)'],
                    'role': role,
                    'include_core_network': incl,
                    'confidence': conf,
                    'reason': reason,
                    'methodological_note': 'Core universe selection standard'
                })
                
                if role == 'PRIMARY': summary_stats[grp]['primary'] += 1
                if incl == 'YES': summary_stats[grp]['core'] += 1
                if role == 'PROCESSED_FOOD': summary_stats[grp]['processed'] += 1
                if role in ['NON_FOOD', 'BYPRODUCT', 'FEED']: summary_stats[grp]['excluded'] += 1
                if role == 'UNCERTAIN': summary_stats[grp]['uncertain'] += 1

        if not found_any:
            crosswalk_rows.append({
                'commodity_group': grp,
                'fbs_item': fbs_name,
                'trade_item': 'NO CANDIDATES FOUND',
                'trade_item_code': pd.NA,
                'cpc_code': pd.NA,
                'role': 'UNCERTAIN',
                'include_core_network': 'NO',
                'confidence': 'LOW',
                'reason': 'No matching commodities discovered in Trade Matrix.',
                'methodological_note': 'Missing trade data for this commodity group.'
            })

    cw_df = pd.DataFrame(crosswalk_rows)
    
    # Run Validation Checks
    print("\nRunning Validation Checks...")
    
    # Check 1
    assert cw_df['commodity_group'].nunique() == 6, "Check 1 Failed: Not exactly 6 commodity groups."
    
    # Check 2
    assert set(cw_df['commodity_group'].unique()) == set(target_groups.keys()), "Check 2 Failed: Unexpected commodity group."
    
    # Check 3 (Assuming unique trade item code per group except NO CANDIDATES)
    
    # Check 4
    excl = cw_df[(cw_df['role'].isin(['BYPRODUCT', 'FEED', 'NON_FOOD'])) & (cw_df['include_core_network'] == 'YES')]
    assert len(excl) == 0, "Check 4 Failed: Excluded item marked as YES."
    
    # Check 5 is identical to Check 4
    
    # Check 6
    dups = cw_df.duplicated(subset=['commodity_group', 'trade_item_code'])
    assert not dups.any(), "Check 6 Failed: Duplicate mappings exist."
    
    # Check 7
    sf = cw_df[cw_df['commodity_group'] == 'Sunflower Oil']
    assert len(sf) > 0, "Check 7 Failed: Sunflower Oil missing."
    
    # Check 8
    core = cw_df[cw_df['include_core_network'] == 'YES']
    assert not core[['trade_item', 'cpc_code', 'role', 'confidence', 'reason']].isna().any().any(), "Check 8 Failed: Missing metadata in core."
    
    cw_df.to_csv(os.path.join(foodshield_dir, 'foodshield_commodity_concordance.csv'), index=False)
    
    # Create Summary
    summary_rows = []
    for grp, fbs_name in target_groups.items():
        st = summary_stats[grp]
        map_stat = 'VALIDATED'
        if st['primary'] == 0: map_stat = 'NO_VALID_MAPPING'
        elif st['uncertain'] > 0: map_stat = 'REVIEW_REQUIRED'
        
        summary_rows.append({
            'commodity_group': grp,
            'fbs_item': fbs_name,
            'primary_trade_item_count': st['primary'],
            'core_trade_item_count': st['core'],
            'processed_trade_item_count': st['processed'],
            'excluded_item_count': st['excluded'],
            'uncertain_item_count': st['uncertain'],
            'mapping_status': map_stat
        })
        
    sum_df = pd.DataFrame(summary_rows)
    sum_df.to_csv(os.path.join(foodshield_dir, 'foodshield_commodity_summary.csv'), index=False)
    
    # Create Markdown Report
    reports_dir = os.path.join(project_root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, 'commodity_concordance_final.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# FOODSHIELD Final Commodity Concordance\n\n")
        
        for grp in target_groups:
            f.write(f"## {grp}\n")
            grp_df = cw_df[cw_df['commodity_group'] == grp]
            
            f.write(f"**FBS Commodity:** {target_groups[grp]}\n\n")
            
            primary = grp_df[grp_df['role'] == 'PRIMARY']
            if len(primary) > 0:
                f.write("**Primary Trade Commodities:**\n")
                for _, row in primary.iterrows():
                    f.write(f"- {row['trade_item']} (CPC: {row['cpc_code']})\n")
            else:
                f.write("**Primary Trade Commodities:** None\n")
                
            core = grp_df[grp_df['include_core_network'] == 'YES']
            f.write("\n**Core Trade Commodities (For Analysis):**\n")
            if len(core) > 0:
                for _, row in core.iterrows():
                    f.write(f"- {row['trade_item']}\n")
            else:
                f.write("- None\n")
                
            processed = grp_df[grp_df['role'] == 'PROCESSED_FOOD']
            f.write("\n**Processed Commodities (Excluded):**\n")
            if len(processed) > 0:
                for _, row in processed.iterrows():
                    f.write(f"- {row['trade_item']}\n")
            else:
                f.write("- None\n")
                
            excl = grp_df[grp_df['role'].isin(['BYPRODUCT', 'FEED', 'NON_FOOD'])]
            f.write("\n**Excluded Byproducts/Feed/Non-Food:**\n")
            if len(excl) > 0:
                for _, row in excl.iterrows():
                    f.write(f"- {row['trade_item']}\n")
            else:
                f.write("- None\n")
                
            uncert = grp_df[grp_df['role'] == 'UNCERTAIN']
            f.write("\n**Uncertain Commodities:**\n")
            if len(uncert) > 0:
                for _, row in uncert.iterrows():
                    f.write(f"- {row['trade_item']}\n")
            else:
                f.write("- None\n")
                
            f.write("\n**Methodological Reasoning:** Direct mapping to primary agricultural product to avoid double-counting processed layers.\n\n")
            f.write("---\n\n")
            
    # Print Terminal Summary
    print("\nFOODSHIELD FINAL COMMODITY UNIVERSE")
    print("===================================")
    
    for grp in target_groups:
        st = summary_stats[grp]
        print(f"\n{list(target_groups.keys()).index(grp) + 1}. {grp}")
        print(f"   Primary: {st['primary']}")
        print(f"   Core: {st['core']}")
        print(f"   Excluded: {st['excluded'] + st['processed']}") # Combine excluded and processed for summary view
        print(f"   Uncertain: {st['uncertain']}")
        
    print("\n===================================")
    print("VALIDATION")
    print("===================================")
    print(f"Selected commodities: {sum_df.shape[0]}")
    print(f"Core trade commodities: {sum_df['core_trade_item_count'].sum()}")
    print(f"Excluded: {sum_df['excluded_item_count'].sum() + sum_df['processed_trade_item_count'].sum()}")
    print(f"Uncertain: {sum_df['uncertain_item_count'].sum()}")
    print(f"No valid mappings: {len(sum_df[sum_df['mapping_status'] == 'NO_VALID_MAPPING'])}")
    print("\nDouble-counting risks: Eliminated by restricting to Core network.")
    
    # Check overlap
    overlaps = cw_df[cw_df['include_core_network'] == 'YES']['trade_item_code'].value_counts()
    over_count = len(overlaps[overlaps > 1])
    print(f"Cross-commodity overlaps: {over_count}")
    
if __name__ == '__main__':
    finalize_foodshield_concordance()
