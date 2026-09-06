import os
import glob
import pandas as pd
import numpy as np
import time

def process_faostat():
    START_YEAR = 2010
    REQUESTED_END_YEAR = 2026
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    raw_dir = os.path.join(project_root, 'data', 'raw')
    processed_dir = os.path.join(project_root, 'data', 'processed')
    
    os.makedirs(processed_dir, exist_ok=True)
    
    target_files = [
        'FoodBalanceSheets_E_All_Data.csv',
        'Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv',
        'Trade_CropsLivestockIndicators_E_All_Data_(Normalized).csv'
    ]
    
    for filename in target_files:
        file_path = os.path.join(raw_dir, filename)
        if not os.path.exists(file_path):
            print(f"Warning: {filename} not found in {raw_dir}. Skipping.")
            continue
            
        print(f"\nProcessing {filename}...")
        start_time = time.time()
        
        is_fbs = 'FoodBalanceSheets' in filename
        chunksize = 250000
        
        first_chunk = True
        
        actual_min_year = float('inf')
        actual_max_year = float('-inf')
        retained_min_year = float('inf')
        retained_max_year = float('-inf')
        
        out_path = os.path.join(processed_dir, filename)
        
        print("  Scanning dataset and filtering chunks...")
        
        with open(out_path, 'w', encoding='utf-8') as f_out:
            pass # Clear file
            
        for chunk in pd.read_csv(file_path, chunksize=chunksize, low_memory=False, encoding='latin1', on_bad_lines='skip'):
            if is_fbs:
                # Wide format
                id_vars = []
                rename_map = {}
                years_in_chunk = set()
                
                for col in chunk.columns:
                    if col.startswith('Y') and len(col) >= 5 and col[1:5].isdigit():
                        yr = int(col[1:5])
                        years_in_chunk.add(yr)
                        actual_min_year = min(actual_min_year, yr)
                        actual_max_year = max(actual_max_year, yr)
                        
                        if len(col) == 5:
                            rename_map[col] = f'Value_{yr}'
                        elif col.endswith('F'):
                            rename_map[col] = f'Flag_{yr}'
                        elif col.endswith('N'):
                            rename_map[col] = f'Note_{yr}'
                    else:
                        id_vars.append(col)
                
                # Unpivot wide format
                chunk_renamed = chunk.rename(columns=rename_map)
                chunk_long = pd.wide_to_long(
                    chunk_renamed, 
                    stubnames=['Value', 'Flag', 'Note'], 
                    i=id_vars, 
                    j='Year', 
                    sep='_'
                ).reset_index()
                
                # Filter rows by year
                df_filtered = chunk_long[
                    (chunk_long['Year'] >= START_YEAR) & 
                    (chunk_long['Year'] <= REQUESTED_END_YEAR)
                ]
                
                # Remove rows where Value, Flag, and Note are all null to save space
                df_filtered = df_filtered.dropna(subset=['Value', 'Flag', 'Note'], how='all')
                
            else:
                # Normalized format
                # Check for Year column
                year_col = 'Year' if 'Year' in chunk.columns else None
                if not year_col:
                    print("  Error: Could not find Year column.")
                    break
                    
                chunk_min_yr = chunk[year_col].min()
                chunk_max_yr = chunk[year_col].max()
                
                if pd.notna(chunk_min_yr): actual_min_year = min(actual_min_year, int(chunk_min_yr))
                if pd.notna(chunk_max_yr): actual_max_year = max(actual_max_year, int(chunk_max_yr))
                
                df_filtered = chunk[
                    (chunk[year_col] >= START_YEAR) & 
                    (chunk[year_col] <= REQUESTED_END_YEAR)
                ]
                
            if not df_filtered.empty:
                f_min = df_filtered['Year'].min()
                f_max = df_filtered['Year'].max()
                if pd.notna(f_min): retained_min_year = min(retained_min_year, int(f_min))
                if pd.notna(f_max): retained_max_year = max(retained_max_year, int(f_max))
                
            df_filtered.to_csv(out_path, mode='a', index=False, header=first_chunk, encoding='utf-8')
            first_chunk = False
            
        end_time = time.time()
        
        if actual_min_year == float('inf'): actual_min_year = "N/A"
        if actual_max_year == float('-inf'): actual_max_year = "N/A"
        if retained_min_year == float('inf'): retained_min_year = "N/A"
        if retained_max_year == float('-inf'): retained_max_year = "N/A"
        
        num_years_retained = 0
        if retained_min_year != "N/A" and retained_max_year != "N/A":
            num_years_retained = retained_max_year - retained_min_year + 1
            
        print(f"  Completed in {end_time - start_time:.2f} seconds")
        print(f"  Requested Year Range: {START_YEAR} - {REQUESTED_END_YEAR}")
        print(f"  Actual Available Year Range: {actual_min_year} - {actual_max_year}")
        print(f"  Latest Available Year: {actual_max_year}")
        print(f"  Number of Years Retained: {num_years_retained}")
        print(f"  Retained Year Range in File: {retained_min_year} - {retained_max_year}")

if __name__ == "__main__":
    process_faostat()
