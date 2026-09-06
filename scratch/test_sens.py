import pandas as pd
import os

DATA_DIR = "data/processed/foodshield"

df_sens_sum = pd.read_csv(os.path.join(DATA_DIR, "foodshield_sensitivity_summary_2010_2023.csv"))
df_sens_trans = pd.read_csv(os.path.join(DATA_DIR, "foodshield_sensitivity_profile_transitions_2010_2023.csv"))

print("Sensitivity summary columns:")
print(df_sens_sum.columns.tolist())
print(df_sens_sum[['experiment', 'mean_replacement_rate', 'type_A_share']])

print("\nTransitions:")
print(df_sens_trans[['experiment', 'A_to_B', 'A_to_C', 'A_to_D', 'C_to_D', 'D_to_D']])
