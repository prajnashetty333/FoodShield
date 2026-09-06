import pandas as pd
import os

def rank_foods():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    processed_dir = os.path.join(project_root, 'data', 'processed')
    outputs_dir = os.path.join(project_root, 'outputs')
    
    fbs_path = os.path.join(processed_dir, 'FoodBalanceSheets_E_All_Data.csv')
    
    print("Loading FBS data...")
    # Load FBS data
    # Columns: Area Code, Area Code (M49), Area, Item Code, Item Code (FBS), Item, Element Code, Element, Unit, Year, Value, Flag
    df = pd.read_csv(fbs_path)
    
    # 1. Filter years 2010-2023
    df = df[(df['Year'] >= 2010) & (df['Year'] <= 2023)]
    
    # 2. Exclude aggregates
    aggregate_names = [
        'Population', 'Grand Total', 'Vegetal Products', 'Animal Products',
        'Cereals - Excluding Beer', 'Starchy Roots', 'Sugar Crops', 'Sugar & Sweeteners',
        'Pulses', 'Treenuts', 'Oilcrops', 'Vegetable Oils', 'Vegetables', 'Fruits - Excluding Wine',
        'Stimulants', 'Spices', 'Alcoholic Beverages', 'Meat', 'Offals', 'Animal fats', 'Eggs',
        'Milk - Excluding Butter', 'Fish, Seafood', 'Aquatic Products, Other', 'Miscellaneous',
        'Infant food' # Sometimes treated as aggregate
    ]
    df = df[~df['Item'].isin(aggregate_names)]
    # Also exclude codes >= 2900 just in case there are others
    df = df[(df['Item Code'] < 2900) & (df['Item Code'] != 2501)]
    
    # 3. Pivot the elements we care about
    # We want to aggregate globally for each item.
    # To do this correctly: for each (Area, Item, Year), we should have the elements as columns.
    
    # The elements we want:
    # 'Food' (1000 t) -> food supply quantity
    # 'Food supply (kcal)' -> calories (if available) or we use kcal/cap/d * population
    # 'Food supply (kcal/capita/day)'
    # 'Protein supply quantity (t)' -> protein
    # 'Protein supply quantity (g/capita/day)'
    
    print("Pivoting data...")
    pivot_df = df.pivot_table(
        index=['Area', 'Item Code', 'Item Code (FBS)', 'Item', 'Year'],
        columns='Element',
        values='Value',
        aggfunc='sum'
    ).reset_index()
    
    # Check if 'Food supply (kcal)' exists and is populated
    has_total_kcal = 'Food supply (kcal)' in pivot_df.columns
    has_total_protein = 'Protein supply quantity (t)' in pivot_df.columns
    
    # If we need population to weight things:
    pop_df = pd.read_csv(fbs_path)
    pop_df = pop_df[(pop_df['Year'] >= 2010) & (pop_df['Year'] <= 2023) & (pop_df['Element'] == 'Total Population - Both sexes')]
    pop_map = pop_df.groupby(['Area', 'Year'])['Value'].mean().to_dict() # value in 1000s
    
    # Add population to pivot_df
    pivot_df['Population (1000s)'] = pivot_df.set_index(['Area', 'Year']).index.map(pop_map)
    
    # Calculate totals if they don't exist
    if not has_total_kcal and 'Food supply (kcal/capita/day)' in pivot_df.columns:
        # kcal/capita/day * population * 365 = total kcal per year
        # population is in 1000s, so pop * 1000 = total people
        pivot_df['Calculated Total Kcal'] = pivot_df['Food supply (kcal/capita/day)'] * (pivot_df['Population (1000s)'] * 1000) * 365
    elif has_total_kcal:
        pivot_df['Calculated Total Kcal'] = pivot_df['Food supply (kcal)'] * 1e6 # million Kcal to Kcal
        
    if not has_total_protein and 'Protein supply quantity (g/capita/day)' in pivot_df.columns:
        # g/capita/day * population * 365 / 1e6 = tonnes per year
        pivot_df['Calculated Total Protein (t)'] = pivot_df['Protein supply quantity (g/capita/day)'] * (pivot_df['Population (1000s)'] * 1000) * 365 / 1e6
    elif has_total_protein:
        pivot_df['Calculated Total Protein (t)'] = pivot_df['Protein supply quantity (t)']
        
    # Food quantity is 'Food' (1000 t). Convert to tonnes.
    if 'Food' in pivot_df.columns:
        pivot_df['Calculated Food (t)'] = pivot_df['Food'] * 1000
    else:
        pivot_df['Calculated Food (t)'] = 0
        
    print("Calculating metrics per item...")
    # Now group by Item to calculate the required metrics
    results = []
    
    grouped = pivot_df.groupby(['Item Code', 'Item Code (FBS)', 'Item'])
    for (icode, fbs_code, item), group in grouped:
        # Number of countries in which the food appears
        countries = group['Area'].nunique()
        # Number of years with available observations (globally)
        years_with_data = group['Year'].nunique()
        
        # Calculate global average/total
        # Global total across all years / years_with_data = annual average global total
        total_kcal_sum = group['Calculated Total Kcal'].sum(skipna=True)
        total_prot_sum = group['Calculated Total Protein (t)'].sum(skipna=True)
        total_food_sum = group['Calculated Food (t)'].sum(skipna=True)
        
        avg_kcal = total_kcal_sum / years_with_data if years_with_data > 0 else 0
        avg_prot = total_prot_sum / years_with_data if years_with_data > 0 else 0
        avg_food = total_food_sum / years_with_data if years_with_data > 0 else 0
        
        results.append({
            'Item Code': icode,
            'Item Code (FBS)': fbs_code,
            'Item': item,
            'Countries': countries,
            'Years': years_with_data,
            'Total/average food supply (t)': avg_food,
            'Total/average calories (kcal)': avg_kcal,
            'Total/average protein (t)': avg_prot
        })
        
    res_df = pd.DataFrame(results)
    
    # Filter out empty items
    res_df = res_df[(res_df['Total/average food supply (t)'] > 0) | (res_df['Total/average calories (kcal)'] > 0)]
    
    # Calculate shares
    total_global_kcal = res_df['Total/average calories (kcal)'].sum()
    total_global_prot = res_df['Total/average protein (t)'].sum()
    
    res_df['Calorie share'] = res_df['Total/average calories (kcal)'] / total_global_kcal
    res_df['Protein share'] = res_df['Total/average protein (t)'] / total_global_prot
    
    # Calculate ranks
    res_df['Food supply rank'] = res_df['Total/average food supply (t)'].rank(ascending=False, method='min')
    res_df['Calorie rank'] = res_df['Total/average calories (kcal)'].rank(ascending=False, method='min')
    res_df['Protein rank'] = res_df['Total/average protein (t)'].rank(ascending=False, method='min')
    
    # Sort by calorie rank
    res_df = res_df.sort_values('Calorie rank')
    
    # Save CSV
    out_csv = os.path.join(outputs_dir, 'fbs_food_importance.csv')
    res_df.to_csv(out_csv, index=False)
    
    # Generate Report
    out_txt = os.path.join(outputs_dir, 'fbs_food_importance_report.txt')
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write("====================================================\n")
        f.write("           FBS FOOD IMPORTANCE REPORT               \n")
        f.write("====================================================\n\n")
        f.write("Methodology:\n")
        f.write("- Timeframe: 2010 to 2023\n")
        f.write("- Aggregation: Values were summed globally per year, then averaged over the available years.\n")
        f.write("- Metric: Calories and protein were calculated as total absolute values (population-weighted indirectly via total summing). Non-food aggregate categories were excluded.\n\n")
        
        f.write("--- Top 30 Foods by Calorie Importance ---\n")
        for i, row in res_df.sort_values('Calorie rank').head(30).iterrows():
            f.write(f"{int(row['Calorie rank'])}. {row['Item']} (Share: {row['Calorie share']*100:.2f}%)\n")
            
        f.write("\n--- Top 30 Foods by Protein Importance ---\n")
        for i, row in res_df.sort_values('Protein rank').head(30).iterrows():
            f.write(f"{int(row['Protein rank'])}. {row['Item']} (Share: {row['Protein share']*100:.2f}%)\n")
            
        f.write("\n--- Top 30 Foods by Food Supply Quantity (t) ---\n")
        for i, row in res_df.sort_values('Food supply rank').head(30).iterrows():
            f.write(f"{int(row['Food supply rank'])}. {row['Item']} (Quantity: {row['Total/average food supply (t)']/1e6:.1f} M t)\n")
            
        f.write("\n--- Most Ubiquitous Foods (Appearing in Largest Number of Countries) ---\n")
        for i, row in res_df.sort_values('Countries', ascending=False).head(15).iterrows():
            f.write(f"- {row['Item']} (Countries: {row['Countries']})\n")
            
        f.write("\n--- Consistently Important Foods (Top 20 in Calories, Protein, AND Food Supply) ---\n")
        consistent = res_df[(res_df['Calorie rank'] <= 20) & (res_df['Protein rank'] <= 20) & (res_df['Food supply rank'] <= 20)]
        for i, row in consistent.sort_values('Calorie rank').iterrows():
            f.write(f"- {row['Item']} (Kcal Rank: {int(row['Calorie rank'])}, Prot Rank: {int(row['Protein rank'])}, Food Rank: {int(row['Food supply rank'])})\n")
            
    print(f"Analysis saved to:\n  - {out_csv}\n  - {out_txt}")

if __name__ == '__main__':
    rank_foods()
