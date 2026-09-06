import pandas as pd
import os
import re

def build_foodshield_concordance():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    processed_dir = os.path.join(project_root, 'data', 'processed')
    foodshield_dir = os.path.join(processed_dir, 'foodshield')
    os.makedirs(foodshield_dir, exist_ok=True)
    
    outputs_dir = os.path.join(project_root, 'outputs')
    trade_path = os.path.join(outputs_dir, 'trade_item_catalog.csv')
    fbs_path = os.path.join(outputs_dir, 'fbs_item_catalog.csv')
    fbs_importance_path = os.path.join(outputs_dir, 'fbs_food_importance.csv')
    
    trade_df = pd.read_csv(trade_path)
    fbs_df = pd.read_csv(fbs_path)
    fbs_imp_df = pd.read_csv(fbs_importance_path) if os.path.exists(fbs_importance_path) else pd.DataFrame()
    
    # Define Tiers
    tiers = {
        "Wheat and products": "Tier 1",
        "Rice and products": "Tier 1",
        "Maize and products": "Tier 1",
        "Potatoes and products": "Tier 1",
        "Cassava and products": "Tier 1",
        "Sorghum and products": "Tier 1",
        "Millet and products": "Tier 1",
        "Pulses, Other and products": "Tier 1",
        "Beans": "Tier 1",
        "Poultry Meat": "Tier 2",
        "Pigmeat": "Tier 2",
        "Bovine Meat": "Tier 2",
        "Freshwater Fish": "Tier 2",
        "Palm Oil": "Tier 3",
        "Soyabean Oil": "Tier 3",
        "Sunflowerseed Oil": "Tier 3",
        "Sugar (Raw Equivalent)": "Tier 4",
        "Soyabeans": "Tier 4",
        "Groundnuts": "Tier 4",
        "Bananas": "Tier 4",
        "Vegetables, other": "Additional",
        "Fruits, other": "Additional",
        "Tomatoes and products": "Additional"
    }
    
    # ---------------------------------------------------------
    # PART A — FOOD UNIVERSE
    # ---------------------------------------------------------
    universe_rows = []
    
    for fbs_item, tier in tiers.items():
        # Get code from fbs_df
        code_match = fbs_df[fbs_df['Item'] == fbs_item]
        food_id = code_match['Item Code (FBS)'].iloc[0] if len(code_match) > 0 else "UNKNOWN"
        
        # Get ranks
        cal_rank = ""
        prot_rank = ""
        food_rank = ""
        trade_rel = "High" # Assume high for now based on global scope
        
        if not fbs_imp_df.empty:
            imp_match = fbs_imp_df[fbs_imp_df['Item'] == fbs_item]
            if len(imp_match) > 0:
                cal_rank = int(imp_match['Calorie rank'].iloc[0]) if not pd.isna(imp_match['Calorie rank'].iloc[0]) else ""
                prot_rank = int(imp_match['Protein rank'].iloc[0]) if not pd.isna(imp_match['Protein rank'].iloc[0]) else ""
                food_rank = int(imp_match['Food supply rank'].iloc[0]) if not pd.isna(imp_match['Food supply rank'].iloc[0]) else ""
                
        # Decision for Additional candidates
        if tier == "Additional":
            reason = "Selected due to extremely high food supply quantity and global ubiquity (top 10 rankings)."
        else:
            reason = f"{tier} core staple / protein / oil / strategic food."
            
        universe_rows.append({
            'food_id': food_id,
            'fbs_food_name': fbs_item,
            'tier': tier,
            'calorie_rank': cal_rank,
            'protein_rank': prot_rank,
            'food_supply_rank': food_rank,
            'international_trade_relevance': trade_rel,
            'selection_status': 'SELECTED',
            'selection_reason': reason
        })
        
    universe_df = pd.DataFrame(universe_rows)
    universe_df.to_csv(os.path.join(foodshield_dir, 'food_universe.csv'), index=False)
    
    # ---------------------------------------------------------
    # PART B to F — TRADE COMMODITY DISCOVERY & CLASSIFICATION
    # ---------------------------------------------------------
    
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
        
    def get_role_and_exclusion(t_lower):
        if match_words(t_lower, ['feed', 'fodder', 'forage', 'pellets']):
            return 'FEED', 'Animal feed'
        if match_words(t_lower, ['bran', 'residues', 'waste', 'cake', 'meal', 'dregs', 'husks', 'straw', 'offal', 'tallow', 'grease']):
            return 'BYPRODUCT', 'Agricultural byproduct'
        if match_words(t_lower, ['live']):
            return 'NON_FOOD', 'Live animal'
        if match_words(t_lower, ['hair', 'wool', 'skins', 'hides', 'bristle', 'feathers', 'stearine', 'industrial', 'seed']):
            return 'NON_FOOD', 'Non-food / Industrial'
        return None, None

    crosswalk_rows = []
    
    for _, u_row in universe_df.iterrows():
        fbs_item = u_row['fbs_food_name']
        fbs_code = u_row['food_id']
        
        found_any = False
        
        for _, trade_row in trade_df.iterrows():
            trade_item = trade_row['Item']
            trade_code = trade_row['Item Code']
            trade_cpc = trade_row['Item Code (CPC)']
            t_lower = trade_item.lower()
            
            is_candidate = False
            
            # Initial broad inclusion rules
            if fbs_item == "Wheat and products":
                is_candidate = match_words(t_lower, ['wheat', 'bulgur', 'macaroni', 'flour', 'pasta', 'bread', 'pastry'], ['buckwheat'])
            elif fbs_item == "Rice and products":
                is_candidate = match_words(t_lower, ['rice', 'paddy', 'milled', 'husked', 'broken'], ['price', 'licorice'])
            elif fbs_item == "Maize and products":
                is_candidate = match_words(t_lower, ['maize', 'corn'], ['peppercorn', 'sweet corn', 'popcorn', 'oil'])
            elif fbs_item == "Potatoes and products":
                is_candidate = match_words(t_lower, ['potato', 'potatoes'], ['sweet potato', 'sweet potatoes'])
            elif fbs_item == "Cassava and products":
                is_candidate = match_words(t_lower, ['cassava', 'tapioca', 'manioc'])
            elif fbs_item == "Sorghum and products":
                is_candidate = match_words(t_lower, ['sorghum'])
            elif fbs_item == "Millet and products":
                is_candidate = match_words(t_lower, ['millet'])
            elif fbs_item == "Pulses, Other and products":
                is_candidate = match_words(t_lower, ['pulse', 'pulses', 'peas', 'pea', 'lentil', 'lentils', 'chickpeas', 'chickpea', 'chick peas', 'cow peas', 'pigeon peas', 'bambara beans', 'vetches', 'lupins'], ['peanut', 'peanuts', 'sweet', 'snow'])
            elif fbs_item == "Beans":
                is_candidate = match_words(t_lower, ['bean', 'beans'], ['soybean', 'soya', 'cocoa', 'coffee', 'locust', 'vanilla', 'castor', 'bambara', 'jelly'])
            elif fbs_item == "Soyabeans":
                is_candidate = match_words(t_lower, ['soya', 'soyabean', 'soybean', 'soybeans', 'soyabeans'], ['oil', 'sauce', 'paste', 'curd'])
            elif fbs_item == "Groundnuts":
                is_candidate = match_words(t_lower, ['groundnut', 'groundnuts', 'peanut', 'peanuts'], ['oil'])
            elif fbs_item == "Poultry Meat":
                is_candidate = match_words(t_lower, ['chicken', 'chickens', 'poultry', 'duck', 'ducks', 'goose', 'geese', 'turkey', 'turkeys'])
            elif fbs_item == "Pigmeat":
                is_candidate = match_words(t_lower, ['pig', 'pigs', 'pork', 'swine', 'bacon', 'ham', 'sausage', 'sausages'], ['guinea pig'])
            elif fbs_item == "Bovine Meat":
                is_candidate = match_words(t_lower, ['bovine', 'beef', 'cattle', 'veal', 'cow', 'cows', 'calve', 'calves', 'buffalo', 'buffaloes'])
            elif fbs_item == "Freshwater Fish":
                is_candidate = match_words(t_lower, ['fish', 'freshwater', 'tilapia', 'carp', 'catfish', 'salmon', 'trout'])
            elif fbs_item == "Palm Oil":
                is_candidate = match_words(t_lower, ['palm oil', 'oil of palm'])
            elif fbs_item == "Soyabean Oil":
                is_candidate = match_words(t_lower, ['soya bean oil', 'soybean oil', 'soya oil'])
            elif fbs_item == "Sunflowerseed Oil":
                is_candidate = match_words(t_lower, ['sunflower', 'sunflower-seed oil', 'sunflower seed oil'], ['seed', 'cake', 'meal']) and 'oil' in t_lower
            elif fbs_item == "Sugar (Raw Equivalent)":
                is_candidate = match_words(t_lower, ['sugar', 'molasses', 'syrup'])
            elif fbs_item == "Bananas":
                is_candidate = match_words(t_lower, ['banana', 'bananas'], ['plantain', 'plantains', 'cooking bananas'])
            elif fbs_item == "Vegetables, other":
                is_candidate = match_words(t_lower, ['vegetable', 'vegetables', 'cabbage', 'lettuce', 'spinach', 'carrot', 'onion', 'garlic', 'cucumber', 'eggplant'], ['oil'])
            elif fbs_item == "Fruits, other":
                is_candidate = match_words(t_lower, ['fruit', 'fruits', 'apple', 'orange', 'grape', 'mango', 'pineapple', 'melon', 'berries', 'berry'])
            elif fbs_item == "Tomatoes and products":
                is_candidate = match_words(t_lower, ['tomato', 'tomatoes'])

            if is_candidate:
                found_any = True
                
                comm_role = 'UNCERTAIN'
                include = 'NA'
                conf = 'LOW'
                meas_level = 'UNKNOWN'
                dc_risk = 'HIGH'
                reason = ''
                map_stat = 'REVIEW_REQUIRED'
                
                # Exclusions check
                excl_role, excl_reason = get_role_and_exclusion(t_lower)
                
                if excl_role:
                    comm_role = excl_role
                    include = 0
                    conf = 'HIGH'
                    meas_level = 'UNKNOWN'
                    dc_risk = 'LOW'
                    reason = excl_reason
                    map_stat = 'EXCLUDED'
                    
                else:
                    # Specific assignment logic
                    if fbs_item == "Sugar (Raw Equivalent)":
                        if 'raw' in t_lower or 'refined' in t_lower or t_lower == 'sugar':
                            comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PRIMARY', 1, 'HIGH', 'PRIMARY_COMMODITY', 'LOW', 'Core sugar', 'VALIDATED')
                        else:
                            comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PROCESSED_FOOD', 'NA', 'MEDIUM', 'PROCESSED_PRODUCT', 'HIGH', 'Secondary sugar product', 'REVIEW_REQUIRED')
                    
                    elif match_words(t_lower, ['flour', 'starch', 'paste', 'sauce', 'juice', 'frozen', 'dried', 'prepared', 'preserved', 'preparations', 'bacon', 'ham', 'sausage']):
                        comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PROCESSED_FOOD', 'NA', 'HIGH', 'PROCESSED_PRODUCT', 'HIGH', 'Processed derivative', 'REVIEW_REQUIRED')
                    
                    elif 'meat' in t_lower or fbs_item in ["Poultry Meat", "Pigmeat", "Bovine Meat"]:
                        if 'meat' in t_lower or match_words(t_lower, ['beef', 'pork', 'chicken', 'duck', 'turkey']):
                            comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PRIMARY', 1, 'HIGH', 'PRIMARY_COMMODITY', 'LOW', 'Primary meat', 'VALIDATED')
                        else:
                            comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('UNCERTAIN', 'NA', 'LOW', 'UNKNOWN', 'HIGH', 'Unclear meat categorization', 'REVIEW_REQUIRED')
                    
                    elif 'oil' in t_lower and fbs_item in ["Palm Oil", "Soyabean Oil", "Sunflowerseed Oil"]:
                        comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PRIMARY', 1, 'HIGH', 'PRIMARY_COMMODITY', 'LOW', 'Primary oil', 'VALIDATED')
                        
                    elif fbs_item == "Freshwater Fish":
                        if match_words(t_lower, ['fillet', 'frozen', 'smoked', 'dried']):
                            comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PROCESSED_FOOD', 'NA', 'MEDIUM', 'PROCESSED_PRODUCT', 'HIGH', 'Processed fish', 'REVIEW_REQUIRED')
                        else:
                            comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PRIMARY', 1, 'MEDIUM', 'PRIMARY_COMMODITY', 'LOW', 'Primary fish', 'VALIDATED')
                            
                    else:
                        # Fallback for primary
                        comm_role, include, conf, meas_level, dc_risk, reason, map_stat = ('PRIMARY', 1, 'MEDIUM', 'PRIMARY_COMMODITY', 'LOW', 'Primary crop/product', 'VALIDATED')
                
                crosswalk_rows.append({
                    'food_id': fbs_code,
                    'fbs_food_name': fbs_item,
                    'trade_item_code': trade_code,
                    'trade_item_name': trade_item,
                    'cpc_code': trade_cpc,
                    'commodity_role': comm_role,
                    'include_in_trade_analysis': include,
                    'confidence': conf,
                    'measurement_level': meas_level,
                    'double_counting_risk': dc_risk,
                    'mapping_reason': reason,
                    'mapping_status': map_stat
                })
        
        if not found_any:
            crosswalk_rows.append({
                'food_id': fbs_code,
                'fbs_food_name': fbs_item,
                'trade_item_code': pd.NA,
                'trade_item_name': pd.NA,
                'cpc_code': pd.NA,
                'commodity_role': 'UNCERTAIN',
                'include_in_trade_analysis': 'NA',
                'confidence': 'LOW',
                'measurement_level': 'UNKNOWN',
                'double_counting_risk': 'LOW',
                'mapping_reason': 'No valid Trade Matrix equivalent found',
                'mapping_status': 'NO_VALID_MATCH'
            })

    cw_df = pd.DataFrame(crosswalk_rows)
    cw_df.to_csv(os.path.join(foodshield_dir, 'commodity_crosswalk.csv'), index=False)
    
    # ---------------------------------------------------------
    # PART H — VALIDATION REPORT
    # ---------------------------------------------------------
    
    num_fbs = universe_df.shape[0]
    num_trade_mapped = cw_df[cw_df['mapping_status'] != 'NO_VALID_MATCH']['trade_item_code'].nunique()
    
    counts = cw_df['commodity_role'].value_counts().to_dict()
    stat_counts = cw_df['mapping_status'].value_counts().to_dict()
    
    no_match_foods = cw_df[cw_df['mapping_status'] == 'NO_VALID_MATCH']['fbs_food_name'].tolist()
    
    # Foods with unusually large numbers of mapped commodities
    item_counts = cw_df[cw_df['mapping_status'] != 'NO_VALID_MATCH'].groupby('fbs_food_name').size()
    large_map_foods = item_counts[item_counts > 10].index.tolist()
    
    dc_cases = cw_df[cw_df['double_counting_risk'] == 'HIGH']
    low_conf = cw_df[cw_df['confidence'] == 'LOW']
    agg_cases = cw_df[cw_df['measurement_level'] == 'AGGREGATE/EQUIVALENT']
    review_cases = cw_df[cw_df['mapping_status'] == 'REVIEW_REQUIRED']
    
    report_path = os.path.join(foodshield_dir, 'concordance_validation_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# FOODSHIELD Commodity Concordance Validation Report\n\n")
        
        f.write(f"**1. Number of selected FBS foods:** {num_fbs}\n")
        f.write(f"**2. Number of trade commodities mapped:** {num_trade_mapped}\n\n")
        
        f.write("**3. Commodity Roles:**\n")
        f.write(f"- PRIMARY: {counts.get('PRIMARY', 0)}\n")
        f.write(f"- PROCESSED_FOOD: {counts.get('PROCESSED_FOOD', 0)}\n")
        f.write(f"- BYPRODUCT: {counts.get('BYPRODUCT', 0)}\n")
        f.write(f"- FEED: {counts.get('FEED', 0)}\n")
        f.write(f"- NON_FOOD: {counts.get('NON_FOOD', 0)}\n")
        f.write(f"- UNCERTAIN: {counts.get('UNCERTAIN', 0)}\n\n")
        
        f.write(f"**4. Validated Mappings:** {stat_counts.get('VALIDATED', 0)}\n")
        f.write(f"**5. Mappings Requiring Review:** {stat_counts.get('REVIEW_REQUIRED', 0)}\n")
        f.write(f"**6. Foods with no valid match:** {len(no_match_foods)} ({', '.join(no_match_foods)})\n\n")
        
        f.write(f"**7. Foods with unusually large mappings (>10):** {', '.join(large_map_foods) if large_map_foods else 'None'}\n\n")
        
        f.write(f"**8. Potential double-counting cases:** {len(dc_cases)} mappings flagged as HIGH risk (due to processing stages).\n\n")
        
        f.write(f"**9. Low-confidence mappings:** {len(low_conf)}\n")
        for _, row in low_conf.head(10).iterrows():
            f.write(f"   - {row['fbs_food_name']} -> {row['trade_item_name']} (Reason: {row['mapping_reason']})\n")
        if len(low_conf) > 10: f.write("   - ...\n")
        
        f.write(f"\n**10. Aggregate/Equivalent mappings:** {len(agg_cases)}\n\n")
        
        f.write(f"**11. Unresolved Methodological Decisions:** {len(review_cases)} items flagged as REVIEW_REQUIRED, mostly concerning whether to include processed forms in the base food supply equivalent.\n\n")
    
    # ---------------------------------------------------------
    # PART J — FINAL TERMINAL SUMMARY
    # ---------------------------------------------------------
    
    print("\nFOODSHIELD STEP 1 COMPLETE\n")
    print(f"Selected foods:\n{num_fbs}\n")
    print(f"Trade commodities discovered:\n{num_trade_mapped}\n")
    print(f"Validated mappings:\n{stat_counts.get('VALIDATED', 0)}\n")
    print(f"Review required:\n{stat_counts.get('REVIEW_REQUIRED', 0)}\n")
    print(f"Excluded:\n{stat_counts.get('EXCLUDED', 0)}\n")
    print(f"No valid match:\n{len(no_match_foods)}\n")
    print(f"Potential double-counting cases:\n{len(dc_cases)}\n")
    
    print("Top unresolved mapping issues (Requires Human Review):")
    # Show the first 10 items marked as REVIEW_REQUIRED
    top_issues = review_cases[['fbs_food_name', 'trade_item_name', 'mapping_reason']].head(10)
    for i, row in top_issues.iterrows():
        print(f"- {row['fbs_food_name']} -> {row['trade_item_name']} : {row['mapping_reason']}")
        
if __name__ == '__main__':
    build_foodshield_concordance()
