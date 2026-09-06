import pandas as pd
import os

DATA_DIR = "data/processed/foodshield"

COMMODITIES = ["Wheat", "Rice", "Maize", "Palm Oil", "Sugar", "Sunflower Oil"]
YEARS = list(range(2011, 2024))

df_res = pd.read_csv(os.path.join(DATA_DIR, "foodshield_resilience_metrics_2010_2023.csv"))

df_base = df_res[
    (df_res['shock_rank'] == 1) & 
    (df_res['year'].isin(YEARS)) & 
    (df_res['capacity_status'] == 'capacity_available') & 
    (df_res['commodity'].isin(COMMODITIES))
].copy()

print(f"Baseline scenario count: {len(df_base)}")

counts = df_base['resilience_profile'].value_counts()
print(counts)

df_pers = pd.read_csv(os.path.join(DATA_DIR, "foodshield_resilience_country_commodity_persistence_2010_2023.csv"))
df_p = df_pers[(df_pers['repeated_type_c'] == 1) | (df_pers['repeated_type_d'] == 1)]
print(f"Persistent C: {(df_pers['repeated_type_c'] == 1).sum()}")
print(f"Persistent D: {(df_pers['repeated_type_d'] == 1).sum()}")
