import pandas as pd
import os
import re

def finalize_commodity_universe():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    processed_dir = os.path.join(project_root, 'data', 'processed')
    foodshield_dir = os.path.join(processed_dir, 'foodshield')
    
    # Read previous concordance
    input_file = os.path.join(foodshield_dir, 'foodshield_commodity_concordance.csv')
    if not os.path.exists(input_file):
        # Fallback if it was saved directly in processed
        input_file = os.path.join(processed_dir, 'foodshield_commodity_concordance.csv')
        
    df = pd.read_csv(input_file)
    
    output_rows = []
    
    target_groups = {
        "Wheat": "WHEAT",
        "Rice": "RICE",
        "Maize": "MAIZE",
        "Palm Oil": "PALM_OIL",
        "Sugar": "SUGAR",
        "Sunflower Oil": "SUNFLOWER_OIL"
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
        
    for _, row in df.iterrows():
        grp = row['commodity_group']
        if grp not in target_groups: continue
        
        trade_item = row['trade_item']
        trade_cpc = row['cpc_code']
        t_lower = trade_item.lower() if pd.notna(trade_item) else ""
        
        c_id = target_groups[grp]
        inc_status = "EXCLUDE_AMBIGUOUS"
        core_net = "NO"
        dc_risk = "LOW"
        reason = ""
        conf = "HIGH"
        note = "Standard decision"
        comm_def = ""
        
        if trade_item == "NO CANDIDATES FOUND":
            inc_status = "EXCLUDE_AMBIGUOUS"
            reason = "No candidates found"
            dc_risk = "LOW"
            
        elif grp == "Wheat":
            comm_def = "Wheat grain"
            if match_words(t_lower, ['bran', 'residues', 'waste', 'straw', 'cake']):
                inc_status, reason = "EXCLUDE_BYPRODUCT", "Agricultural byproduct"
            elif match_words(t_lower, ['flour', 'pasta', 'macaroni', 'pastry', 'bread', 'bulgur', 'groats']):
                inc_status, reason = "EXCLUDE_PROCESSED", "Processed wheat product"
            elif t_lower == 'wheat':
                inc_status, reason, core_net = "CORE", "Primary commodity", "YES"
            else:
                inc_status, reason, conf = "REVIEW", "Uncertain wheat classification", "LOW"
                
        elif grp == "Rice":
            comm_def = "Rice, paddy or milled as primary grain"
            if match_words(t_lower, ['bran', 'residues', 'waste', 'straw', 'cake']):
                inc_status, reason = "EXCLUDE_BYPRODUCT", "Agricultural byproduct"
            elif match_words(t_lower, ['flour', 'preparations', 'beverages', 'broken', 'milled', 'husked']):
                inc_status, reason = "EXCLUDE_PROCESSED", "Processed/milled derivative (excluded to avoid counting multiple stages)"
            elif t_lower == 'rice' or 'paddy' in t_lower:
                inc_status, reason, core_net = "CORE", "Primary commodity", "YES"
            else:
                inc_status, reason, conf = "REVIEW", "Uncertain rice classification", "LOW"
                
        elif grp == "Maize":
            comm_def = "Maize (corn) grain"
            if match_words(t_lower, ['bran', 'residues', 'waste', 'cake', 'feed', 'fodder', 'forage', 'pellets']):
                inc_status, reason = "EXCLUDE_FEED", "Byproduct or feed"
                if 'bran' in t_lower or 'cake' in t_lower: inc_status = "EXCLUDE_BYPRODUCT"
            elif match_words(t_lower, ['flour', 'starch', 'germ', 'preparations', 'sweet corn', 'popcorn']):
                inc_status, reason = "EXCLUDE_PROCESSED", "Processed derivative or vegetable corn"
            elif t_lower == 'maize (corn)':
                inc_status, reason, core_net = "CORE", "Primary commodity", "YES"
            else:
                inc_status, reason, conf = "REVIEW", "Uncertain maize classification", "LOW"
                
        elif grp == "Palm Oil":
            comm_def = "Palm oil (excluding kernel oil)"
            if match_words(t_lower, ['kernel', 'cake', 'meal']):
                inc_status, reason = "EXCLUDE_BYPRODUCT", "Kernel/cake byproduct"
            elif t_lower == 'palm oil':
                inc_status, reason, core_net = "CORE", "Primary commodity", "YES"
            else:
                inc_status, reason, conf = "REVIEW", "Uncertain palm classification", "LOW"
                
        elif grp == "Sugar":
            comm_def = "Centrifugal sugar (raw equivalent)"
            if match_words(t_lower, ['maple', 'sugar beet', 'sugar cane']):
                inc_status, reason = "EXCLUDE_UNRELATED", "Raw crop before processing"
            elif match_words(t_lower, ['confectionery', 'preserved', 'preparations', 'syrups n.e.c.', 'flavouring']):
                inc_status, reason = "EXCLUDE_PROCESSED", "Processed sugar product"
            elif match_words(t_lower, ['molasses']):
                inc_status, reason = "EXCLUDE_BYPRODUCT", "Processing byproduct"
            elif t_lower == 'refined sugar':
                inc_status, reason = "EXCLUDE_PROCESSED", "Refined sugar (excluded to avoid double counting with raw equivalent)"
            elif t_lower in ['raw cane or beet sugar (centrifugal only)', 'cane sugar, non-centrifugal']:
                inc_status, reason, core_net = "CORE", "Primary raw equivalent commodity", "YES"
            else:
                inc_status, reason, conf = "REVIEW", "Uncertain sugar classification", "LOW"
                
        elif grp == "Sunflower Oil":
            comm_def = "Crude or refined sunflower oil"
            if match_words(t_lower, ['cake', 'meal']) or (match_words(t_lower, ['seed']) and not match_words(t_lower, ['oil'])):
                inc_status, reason = "EXCLUDE_BYPRODUCT", "Seed or cake (Not oil)"
            elif match_words(t_lower, ['sunflower-seed oil', 'sunflower oil', 'oil of sunflower']):
                inc_status, reason, core_net = "CORE", "Primary commodity", "YES"
            else:
                inc_status, reason, conf = "REVIEW", "Uncertain sunflower classification", "LOW"

        # Apply Double Counting Logic: Any processed derivative risks double counting if included.
        if "EXCLUDE_PROCESSED" in inc_status:
            dc_risk = "HIGH"
            note = "High risk of double-counting if merged with CORE primary commodity."

        output_rows.append({
            'commodity_id': c_id,
            'commodity_group': grp,
            'fbs_item': row['fbs_item'],
            'trade_item': trade_item,
            'trade_item_code': row['trade_item_code'],
            'cpc_code': trade_cpc,
            'commodity_definition': comm_def,
            'inclusion_status': inc_status,
            'core_network': core_net,
            'confidence': conf,
            'double_counting_risk': dc_risk,
            'reason': reason,
            'methodological_note': note
        })

    out_df = pd.DataFrame(output_rows)
    
    # Task 9 - Validation Checks
    print("\nRunning Automated Validation Checks...")
    failed = False
    
    # 1. Any commodity outside the six selected commodities appears as CORE.
    core_df = out_df[out_df['inclusion_status'] == 'CORE']
    allowed_ids = set(target_groups.values())
    bad_cores = core_df[~core_df['commodity_id'].isin(allowed_ids)]
    if len(bad_cores) > 0:
        print("FAIL: Commodity outside the 6 target groups appears as CORE!")
        failed = True
        
    # 2 & 3. Missing CPC code or missing trade item in CORE
    missing_cpc = core_df[core_df['cpc_code'].isna()]
    if len(missing_cpc) > 0:
        print("FAIL: Missing CPC code in CORE records!")
        failed = True
    missing_trade = core_df[core_df['trade_item'].isna()]
    if len(missing_trade) > 0:
        print("FAIL: Missing trade item in CORE records!")
        failed = True
        
    # 4. Duplicate CORE mappings
    dups = core_df.duplicated(subset=['commodity_id', 'trade_item_code'])
    if dups.any():
        print("FAIL: Duplicate CORE mappings exist unexpectedly!")
        failed = True
        
    # 5. A commodity has zero CORE trade items.
    core_counts = core_df['commodity_id'].value_counts()
    for cid in allowed_ids:
        if cid not in core_counts or core_counts[cid] == 0:
            print(f"FAIL: Commodity {cid} has zero CORE trade items!")
            failed = True
            
    # 6. include_core_network and inclusion_status contradict each other
    contradict = out_df[((out_df['inclusion_status'] == 'CORE') & (out_df['core_network'] != 'YES')) | 
                        ((out_df['inclusion_status'] != 'CORE') & (out_df['core_network'] == 'YES'))]
    if len(contradict) > 0:
        print("FAIL: core_network and inclusion_status contradict each other!")
        failed = True
        
    # 7. HIGH double-counting risk exists for a CORE mapping.
    high_dc_core = core_df[core_df['double_counting_risk'] == 'HIGH']
    if len(high_dc_core) > 0:
        print("FAIL: HIGH double-counting risk exists for a CORE mapping!")
        failed = True
        
    # 8. An excluded commodity accidentally appears in the core-only file.
    if len(core_df[core_df['inclusion_status'].str.contains('EXCLUDE')]) > 0:
        print("FAIL: An excluded commodity accidentally appears in the core-only file!")
        failed = True
        
    if not failed:
        print("All Validation Checks Passed.")
        
    # Write files
    out_df.to_csv(os.path.join(processed_dir, 'foodshield_commodity_universe.csv'), index=False)
    core_df.to_csv(os.path.join(processed_dir, 'foodshield_core_commodities.csv'), index=False)
    
    # Task 7 - Methodology File
    methodology = """# FOODSHIELD Commodity Methodology

## WHEAT
**Definition:** Wheat grain representing the primary traded staple.
**Core trade representation:** Wheat (CPC: '0111)
**Exclusions:** Wheat flour, pasta, bakery products (Processed); bran (Byproduct).
**Double-counting rationale:** Excluding flour and processed foods ensures that downstream processing volumes do not artificially inflate the physical supply dependency.
**Limitations:** Assumes primary wheat grain trade dominates the physical dependency relationship.

## RICE
**Definition:** Rice (paddy or milled) representing the primary grain.
**Core trade representation:** Rice (CPC: '0113)
**Exclusions:** Husked/milled splits (where redundant), rice flour, beverages.
**Double-counting rationale:** Only the aggregate 'Rice' category is included as the primary node. Sub-stages are excluded to avoid counting the same harvest twice.
**Limitations:** Data granularity forces a combined rice view.

## MAIZE
**Definition:** Maize (corn) grain.
**Core trade representation:** Maize (corn) (CPC: '0112)
**Exclusions:** Maize flour, starch, sweet corn, forage (Feed).
**Double-counting rationale:** Excluding downstream processing products like starch and flour. Feed maize is excluded as the focus is human food supply.
**Limitations:** Differentiating human-food maize from feed maize at the border is difficult; 'Maize (corn)' may include some dual-purpose flows.

## PALM OIL
**Definition:** Crude or refined palm oil.
**Core trade representation:** Palm oil (CPC: '2165)
**Exclusions:** Palm kernel, palm kernel oil.
**Double-counting rationale:** Palm oil and palm kernel oil are distinct commodities with distinct markets.
**Limitations:** None significant.

## SUGAR
**Definition:** Centrifugal sugar in raw equivalent terms.
**Core trade representation:** Raw cane or beet sugar (centrifugal only) (CPC: '2351f), Cane sugar, non-centrifugal.
**Exclusions:** Refined sugar, molasses, sugar crops (beet/cane), confectionery.
**Double-counting rationale:** Treating raw sugar as the core bottleneck and excluding refined sugar prevents counting the sugar twice (once entering the refinery, once exiting).
**Limitations:** Some countries might exclusively import refined sugar rather than raw, potentially undercounting their dependency if refined is strictly excluded.

## SUNFLOWER OIL
**Definition:** Crude or refined sunflower oil.
**Core trade representation:** Sunflower-seed oil, crude (CPC: '21631.01)
**Exclusions:** Sunflower seed, cake, meal.
**Double-counting rationale:** Seed and cake are structurally distinct from the pressed oil market.
**Limitations:** Crude vs refined distinction.
"""
    with open(os.path.join(processed_dir, 'foodshield_commodity_methodology.md'), 'w', encoding='utf-8') as f:
        f.write(methodology)
        
    # Task 8 - Validation Report
    num_sel = 6
    core_items = out_df[out_df['inclusion_status'] == 'CORE'].groupby('commodity_group')['trade_item'].apply(list).to_dict()
    num_ex_proc = len(out_df[out_df['inclusion_status'] == 'EXCLUDE_PROCESSED'])
    num_ex_by = len(out_df[out_df['inclusion_status'] == 'EXCLUDE_BYPRODUCT'])
    num_ex_feed = len(out_df[out_df['inclusion_status'].isin(['EXCLUDE_FEED', 'EXCLUDE_NONFOOD'])])
    num_review = len(out_df[out_df['inclusion_status'] == 'REVIEW'])
    num_dc = len(out_df[out_df['double_counting_risk'] == 'HIGH'])
    
    val_rep = f"""FOODSHIELD COMMODITY VALIDATION REPORT

1. Number of selected commodities: {num_sel}

2. Core trade commodities by commodity:
   - Wheat: {', '.join(core_items.get('Wheat', []))}
   - Rice: {', '.join(core_items.get('Rice', []))}
   - Maize: {', '.join(core_items.get('Maize', []))}
   - Palm Oil: {', '.join(core_items.get('Palm Oil', []))}
   - Sugar: {', '.join(core_items.get('Sugar', []))}
   - Sunflower Oil: {', '.join(core_items.get('Sunflower Oil', []))}

3. Excluded processed commodities: {num_ex_proc}

4. Excluded by-products: {num_ex_by}

5. Excluded feed/non-food commodities: {num_ex_feed}

6. Ambiguous/review items: {num_review}

7. Double-counting risks: {num_dc} high-risk items excluded.

8. Final methodological decisions: Enforced strict core primary representations.

9. Remaining limitations: Refined sugar exclusion may underrepresent total sugar flows for countries without domestic refineries.

10. Final recommendation:
   Is the commodity universe ready for country-level analysis? YES.

Commodity | FBS Item | Core Trade Item(s) | CPC | Status | Confidence
-----------------------------------------------------------------------
"""
    for grp in target_groups:
        items = out_df[(out_df['commodity_group'] == grp) & (out_df['inclusion_status'] == 'CORE')]
        for _, row in items.iterrows():
            val_rep += f"{grp} | {row['fbs_item']} | {row['trade_item']} | {row['cpc_code']} | CORE | HIGH\n"

    with open(os.path.join(processed_dir, 'foodshield_commodity_validation_report.txt'), 'w', encoding='utf-8') as f:
        f.write(val_rep)
        
    # Terminal Summary
    print("\n====================================================")
    print("       FOODSHIELD STEP 3C COMPLETE")
    print("====================================================\n")
    print("Selected commodities: 6\n")
    
    total_core = 0
    total_exc = 0
    
    for grp, cid in target_groups.items():
        grp_df = out_df[out_df['commodity_id'] == cid]
        c = len(grp_df[grp_df['inclusion_status'] == 'CORE'])
        e = len(grp_df[grp_df['inclusion_status'].str.contains('EXCLUDE')])
        total_core += c
        total_exc += e
        
        print(f"{cid}:")
        print(f"  Core trade items: {c}")
        print(f"  Excluded: {e}\n")
        
    print("----------------------------------------------------\n")
    print(f"Total CORE trade commodities: {total_core}")
    print(f"Total EXCLUDED: {total_exc}")
    print(f"High double-counting risks among CORE: {len(core_df[core_df['double_counting_risk'] == 'HIGH'])}")
    print(f"Unresolved REVIEW items: {num_review}\n")
    print("----------------------------------------------------\n")
    print("Output:")
    print("foodshield_commodity_universe.csv")
    print("foodshield_core_commodities.csv")
    print("foodshield_commodity_methodology.md")
    print("foodshield_commodity_validation_report.txt\n")
    print("====================================================")
    print("READY FOR STEP 4: COUNTRY UNIVERSE")
    print("====================================================")

if __name__ == '__main__':
    finalize_commodity_universe()
