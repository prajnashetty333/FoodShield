import os
import pandas as pd
import time

def process_catalog(filepath, item_code_col, alt_code_col):
    """
    Reads a large CSV in chunks and extracts unique item metadata.
    Returns a DataFrame representing the catalog.
    """
    catalog_dict = {}
    
    # Read only necessary columns
    usecols = ['Item Code', alt_code_col, 'Item', 'Element', 'Unit']
    
    print(f"Reading {os.path.basename(filepath)}...")
    start_time = time.time()
    
    for chunk in pd.read_csv(filepath, usecols=usecols, chunksize=500000, low_memory=False, encoding='utf-8'):
        unique_rows = chunk.drop_duplicates()
        for _, row in unique_rows.iterrows():
            key = (row['Item Code'], row[alt_code_col], row['Item'])
            if key not in catalog_dict:
                catalog_dict[key] = {'Element': set(), 'Unit': set()}
            catalog_dict[key]['Element'].add(str(row['Element']))
            catalog_dict[key]['Unit'].add(str(row['Unit']))
            
    print(f"  Finished in {time.time() - start_time:.2f} seconds.")
    
    # Convert dict to DataFrame
    rows = []
    for (icode, alt_code, item), meta in catalog_dict.items():
        rows.append({
            'Item Code': icode,
            alt_code_col: alt_code,
            'Item': item,
            'Elements': ' | '.join(sorted(meta['Element'])),
            'Units': ' | '.join(sorted(meta['Unit']))
        })
        
    return pd.DataFrame(rows)

def build_catalogs():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    processed_dir = os.path.join(project_root, 'data', 'processed')
    outputs_dir = os.path.join(project_root, 'outputs')
    
    os.makedirs(outputs_dir, exist_ok=True)
    
    trade_path = os.path.join(processed_dir, 'Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv')
    fbs_path = os.path.join(processed_dir, 'FoodBalanceSheets_E_All_Data.csv')
    
    # Process catalogs
    trade_df = process_catalog(trade_path, 'Item Code', 'Item Code (CPC)')
    fbs_df = process_catalog(fbs_path, 'Item Code', 'Item Code (FBS)')
    
    # Save to CSV
    out_trade = os.path.join(outputs_dir, 'trade_item_catalog.csv')
    out_fbs = os.path.join(outputs_dir, 'fbs_item_catalog.csv')
    
    trade_df.to_csv(out_trade, index=False, encoding='utf-8')
    fbs_df.to_csv(out_fbs, index=False, encoding='utf-8')
    
    # Generate Summary
    num_trade = len(trade_df)
    num_fbs = len(fbs_df)
    
    trade_codes = set(trade_df['Item Code'].astype(str))
    fbs_codes = set(fbs_df['Item Code'].astype(str))
    code_intersection = trade_codes.intersection(fbs_codes)
    
    trade_names = set(trade_df['Item'].str.lower())
    fbs_names = set(fbs_df['Item'].str.lower())
    name_intersection = trade_names.intersection(fbs_names)
    
    summary_path = os.path.join(outputs_dir, 'item_catalog_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("====================================================\n")
        f.write("           ITEM CATALOG SUMMARY REPORT              \n")
        f.write("====================================================\n\n")
        
        f.write(f"Number of unique Trade Matrix commodities: {num_trade}\n")
        f.write(f"Number of unique FBS commodities: {num_fbs}\n\n")
        
        f.write("--- Trade Matrix Examples ---\n")
        for _, row in trade_df.head(5).iterrows():
            f.write(f"  Code: {row['Item Code']} | CPC: {row['Item Code (CPC)']} | Item: {row['Item']} | Units: {row['Units']}\n")
            
        f.write("\n--- FBS Examples ---\n")
        for _, row in fbs_df.head(5).iterrows():
            f.write(f"  Code: {row['Item Code']} | FBS Code: {row['Item Code (FBS)']} | Item: {row['Item']} | Units: {row['Units']}\n")
            
        f.write("\n--- Structural Analysis ---\n")
        f.write(f"Exact 'Item Code' overlaps: {len(code_intersection)}\n")
        f.write("Do exact item-code relationships appear possible? ")
        if len(code_intersection) > 0:
            f.write("Yes, there is some overlap in primary 'Item Code'. ")
            if len(code_intersection) < min(num_trade, num_fbs) * 0.1:
                f.write("However, the overlap is very small (< 10%), suggesting the codes might not map directly for most items.\n")
            else:
                f.write("There is significant overlap to explore.\n")
        else:
            f.write("No, there are zero exact matches in primary 'Item Code'.\n")
            
        f.write("\nAre CPC codes structurally useful for mapping to FBS codes?\n")
        trade_cpc_sample = list(trade_df['Item Code (CPC)'].dropna())[:5]
        fbs_code_sample = list(fbs_df['Item Code (FBS)'].dropna())[:5]
        f.write(f"  Sample CPC codes: {trade_cpc_sample}\n")
        f.write(f"  Sample FBS codes: {fbs_code_sample}\n")
        f.write("  Observation: CPC codes typically use a numeric structure with decimals/letters (e.g., '0111', 'F1982'), while FBS codes often start with 'S' followed by a number (e.g., 'S2511'). Direct 1:1 mapping between these string codes is unlikely without an external crosswalk.\n")
        
        f.write(f"\n--- Name Comparisons (CANDIDATES ONLY) ---\n")
        f.write(f"Common/similar item names: {len(name_intersection)} exact matches found (case-insensitive).\n")
        f.write("Examples of common names:\n")
        for name in list(name_intersection)[:10]:
            f.write(f"  - {name.title()}\n")
            
        f.write("\nWARNING: These are candidate mappings only. Manual validation or an external crosswalk is required to confirm relationships.\n")
        
    print(f"\nCatalogs built successfully.")
    print(f"Trade catalog saved to: {out_trade}")
    print(f"FBS catalog saved to: {out_fbs}")
    print(f"Summary saved to: {summary_path}")
    
    print("\nSummary Statistics:")
    print(f" - Trade Matrix items: {num_trade}")
    print(f" - FBS items: {num_fbs}")

if __name__ == '__main__':
    build_catalogs()
