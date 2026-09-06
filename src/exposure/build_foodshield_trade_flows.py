import pandas as pd
import numpy as np
import os
import time

def process_trade_data():
    raw_file = 'data/raw/Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv'
    country_file = 'data/processed/foodshield/foodshield_country_universe.csv'
    output_csv = 'data/processed/foodshield/foodshield_trade_flows.csv'
    report_file = 'reports/validation/FOODSHIELD_STEP_5B_TRADE_FLOW_VALIDATION_REPORT.md'
    summary_file = 'data/processed/foodshield/foodshield_trade_flow_summary.csv'

    os.makedirs('data/processed/foodshield', exist_ok=True)

    # Load country universe
    df_countries = pd.read_csv(country_file)
    valid_reporters = df_countries[df_countries['is_trade_reporter'] == 'YES']['country_code'].tolist()
    valid_partners = df_countries[df_countries['is_trade_partner'] == 'YES']['country_code'].tolist()
    
    country_map = dict(zip(df_countries['country_code'], df_countries['standardized_country_name']))

    # Locked commodity universe
    trade_items = {
        15: ('Wheat', "'0111"),
        27: ('Rice', "'0113"),
        56: ('Maize', "'0112"),
        257: ('Palm Oil', "'2165"),
        162: ('Sugar', "'2351f"),
        163: ('Sugar', "'23511.02"),
        268: ('Sunflower Oil', "'21631.01")
    }
    valid_items = list(trade_items.keys())

    chunksize = 1_000_000
    chunks = []
    
    total_rows_raw = 0
    start_time = time.time()
    
    print("Reading data in chunks...")
    for chunk in pd.read_csv(raw_file, chunksize=chunksize, encoding='latin1'):
        total_rows_raw += len(chunk)
        
        # Filter commodities
        chunk = chunk[chunk['Item Code'].isin(valid_items)]
        
        # Filter elements (keep only imports)
        chunk = chunk[chunk['Element'].isin(['Import quantity', 'Import value'])]
        
        # Filter countries
        chunk = chunk[chunk['Reporter Country Code'].isin(valid_reporters)]
        chunk = chunk[chunk['Partner Country Code'].isin(valid_partners)]
        
        # Keep only required columns
        cols_to_keep = [
            'Reporter Country Code', 'Partner Country Code', 
            'Item Code', 'Item', 'Item Code (CPC)', 'Year', 
            'Element', 'Unit', 'Value', 'Flag'
        ]
        chunk = chunk[cols_to_keep]
        
        chunks.append(chunk)
        print(f"Processed {total_rows_raw} rows...")
        
    df_filtered = pd.concat(chunks, ignore_index=True)
    rows_after_filter = len(df_filtered)
    print(f"Total rows after filtering: {rows_after_filter}")
    
    # Process dataframe: pivot quantity and value
    df_q = df_filtered[df_filtered['Element'] == 'Import quantity'].copy()
    df_q = df_q.rename(columns={'Value': 'quantity', 'Unit': 'quantity_unit', 'Flag': 'flag_quantity'})
    df_q = df_q.drop(columns=['Element'])
    
    df_v = df_filtered[df_filtered['Element'] == 'Import value'].copy()
    df_v = df_v.rename(columns={'Value': 'trade_value', 'Unit': 'value_unit', 'Flag': 'flag_value'})
    df_v = df_v.drop(columns=['Element'])
    
    # Merge
    merge_keys = ['Reporter Country Code', 'Partner Country Code', 'Item Code', 'Item', 'Item Code (CPC)', 'Year']
    df_final = pd.merge(df_q, df_v, on=merge_keys, how='outer')
    
    # Map additional columns
    df_final['reporter_country_code'] = df_final['Reporter Country Code']
    df_final['reporter_country_name'] = df_final['reporter_country_code'].map(country_map)
    df_final['partner_country_code'] = df_final['Partner Country Code']
    df_final['partner_country_name'] = df_final['partner_country_code'].map(country_map)
    df_final['commodity'] = df_final['Item Code'].map(lambda x: trade_items[x][0])
    df_final['trade_item_code'] = df_final['Item Code']
    df_final['trade_item_name'] = df_final['Item']
    df_final['cpc_code'] = df_final['Item Code (CPC)']
    df_final['year'] = df_final['Year']
    df_final['element'] = 'Import'
    
    def combine_flags(q, v):
        q = str(q) if pd.notna(q) else ""
        v = str(v) if pd.notna(v) else ""
        if q and v: return f"q:{q},v:{v}"
        if q: return f"q:{q}"
        if v: return f"v:{v}"
        return ""

    df_final['flag'] = df_final.apply(lambda row: combine_flags(row['flag_quantity'], row['flag_value']), axis=1)
    
    # Keep final columns
    final_cols = [
        'reporter_country_code', 'reporter_country_name',
        'partner_country_code', 'partner_country_name',
        'commodity', 'trade_item_code', 'trade_item_name', 'cpc_code',
        'year', 'element', 'quantity', 'quantity_unit', 
        'trade_value', 'value_unit', 'flag'
    ]
    df_final = df_final[final_cols]
    
    # Diagnostics & Metrics
    total_reporters = df_final['reporter_country_code'].nunique()
    total_partners = df_final['partner_country_code'].nunique()
    df_final['pair'] = df_final['reporter_country_code'].astype(str) + '_' + df_final['partner_country_code'].astype(str)
    total_pairs = df_final['pair'].nunique()
    total_commodities = df_final['commodity'].nunique()
    total_trade_items = df_final['trade_item_code'].nunique()
    year_min = df_final['year'].min()
    year_max = df_final['year'].max()
    
    total_trade_value = df_final['trade_value'].sum(skipna=True)
    total_trade_quantity = df_final['quantity'].sum(skipna=True)
    
    missing_qty = df_final['quantity'].isna().sum()
    missing_val = df_final['trade_value'].isna().sum()
    zero_qty = (df_final['quantity'] == 0).sum()
    zero_val = (df_final['trade_value'] == 0).sum()
    
    # Self-trade check
    self_trade = df_final[df_final['reporter_country_code'] == df_final['partner_country_code']]
    num_self_trade = len(self_trade)
    
    # Duplicates check
    dupes_item = df_final.duplicated(subset=['reporter_country_code', 'partner_country_code', 'trade_item_code', 'year'], keep=False)
    num_dupes_item = dupes_item.sum()
    
    dupes_comm = df_final.duplicated(subset=['reporter_country_code', 'partner_country_code', 'commodity', 'year'], keep=False)
    num_dupes_comm = dupes_comm.sum()
    
    # Output to CSV
    df_final.drop(columns=['pair'], inplace=True)
    df_final.to_csv(output_csv, index=False)
    print(f"Saved {len(df_final)} rows to {output_csv}")
    
    # Write validation report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# FOODSHIELD STEP 5B: TRADE FLOW VALIDATION REPORT\n\n")
        f.write("## 1. Source Information\n")
        f.write(f"- Source file: `{raw_file}`\n")
        f.write(f"- Source row count: {total_rows_raw}\n")
        f.write(f"- Filtered row count: {rows_after_filter} (Import Quantity + Import Value records)\n")
        f.write(f"- Final analytical dataset row count: {len(df_final)}\n\n")
        
        f.write("## 2. Coverage Metrics\n")
        f.write(f"- Number of reporters: {total_reporters}\n")
        f.write(f"- Number of partners: {total_partners}\n")
        f.write(f"- Number of bilateral pairs: {total_pairs}\n")
        f.write(f"- Number of commodities: {total_commodities}\n")
        f.write(f"- Number of trade-item representations: {total_trade_items}\n")
        f.write(f"- Year range: {year_min} to {year_max}\n\n")
        
        f.write("## 3. Aggregate Totals\n")
        f.write(f"- Total trade value (1000 USD): {total_trade_value:,.2f}\n")
        f.write(f"- Total trade quantity (tonnes): {total_trade_quantity:,.2f}\n\n")
        
        f.write("## 4. Diagnostics\n")
        f.write(f"- Missing quantity: {missing_qty}\n")
        f.write(f"- Missing value: {missing_val}\n")
        f.write(f"- Zero quantity: {zero_qty}\n")
        f.write(f"- Zero value: {zero_val}\n")
        f.write(f"- Self-trade records (Reporter == Partner): {num_self_trade}\n")
        f.write(f"- Duplicate records at Trade-Item level: {num_dupes_item}\n")
        f.write(f"- Duplicate records at Commodity level (due to Sugar items 162/163): {num_dupes_comm}\n\n")
        
        f.write("## 5. Methodological Decisions & Remarks\n")
        f.write("- **Import Direction:** Kept only 'Import quantity' and 'Import value' elements from FAOSTAT. They were merged on common keys so each row has a quantity and trade_value.\n")
        f.write("- **Missing/Zero:** Left them as NaN/0 instead of removing them to avoid losing other valid information in the same row.\n")
        f.write("- **Self-Trade:** Identified but not removed. Can be filtered out downstream if needed.\n")
        f.write("- **Sugar Aggregation:** Items 162 and 163 both map to Sugar. The dataset retains `trade_item_code` for auditability. Aggregating to Commodity level will require summing 162 and 163 where applicable.\n\n")

    # Generate country coverage summary table
    # Commodity | Reporter Countries | Partner Countries | Bilateral Pairs | Years | Missing/zero observations
    summary_data = []
    for comm in df_final['commodity'].unique():
        df_c = df_final[df_final['commodity'] == comm]
        missing_zero = (df_c['quantity'].isna() | df_c['trade_value'].isna() | (df_c['quantity'] == 0) | (df_c['trade_value'] == 0)).sum()
        summary_data.append({
            'Commodity': comm,
            'Reporter Countries': df_c['reporter_country_code'].nunique(),
            'Partner Countries': df_c['partner_country_code'].nunique(),
            'Bilateral Pairs': (df_c['reporter_country_code'].astype(str) + '_' + df_c['partner_country_code'].astype(str)).nunique(),
            'Years Available': df_c['year'].nunique(),
            'Missing/Zero Observations': missing_zero
        })
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv(summary_file, index=False)

if __name__ == "__main__":
    process_trade_data()
