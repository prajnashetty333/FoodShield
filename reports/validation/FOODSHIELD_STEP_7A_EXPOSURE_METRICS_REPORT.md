# FOODSHIELD STEP 7A EXPOSURE METRICS REPORT

## 1. Objective
Step 7A establishes the fundamental exposure metrics for six key agricultural commodities across 220 countries from 2010 to 2023. This step correctly defines and calculates two distinct dimensions of exposure: physical import dependence (domestic supply exposure) and foreign supplier concentration, without combining them into a single arbitrary risk score.

## 2. Data sources
- `data/processed/foodshield/foodshield_country_universe.csv`
- `data/processed/foodshield/foodshield_bilateral_trade_2010_2023.csv`
- `data/processed/foodshield/foodshield_country_commodity_exposure_2010_2023.csv`
- `data/processed/foodshield/foodshield_supplier_shares_2010_2023.csv`
- `data/processed/FoodBalanceSheets_E_All_Data.csv`

## 3. Analytical period
2010–2023 (14 years).

## 4. Commodity coverage
Exactly six commodities:
- Maize
- Palm Oil
- Rice
- Sugar
- Sunflower Oil
- Wheat

## 5. Country coverage
The validated 220-country/economy universe. 
- 178 countries are actively represented with trade data in these commodities.
- 42 countries have no trade data in the trade matrix for these specific commodities.
- FBS data covers 158 of these countries (which successfully merge on M49 country code).

## 6. FBS mapping
- **Wheat**: mapped to `Wheat and products` (2511)
- **Rice**: mapped to `Rice and products` (2807)
- **Maize**: mapped to `Maize and products` (2514)
- **Palm Oil**: mapped to `Palm Oil` (2577)
- **Sugar**: mapped to `Sugar (Raw Equivalent)` (2542)
- **Sunflower Oil**: mapped to `Sunflowerseed Oil` (2573)
*Note: A detailed mapping is maintained in `foodshield_fbs_exposure_mapping.csv`.*

## 7. Trade exposure metrics
- **Total imports**: `total_import_quantity_tonnes` and `total_import_value_1000_usd` are retained directly from the Step 6A output to represent total absolute physical and financial trade exposure.
- **Supplier count**: Total number of foreign origins with positive imports.
- **Largest supplier share**: Quantity share [0-1] of the single largest supplier.
- **Top-3 share**: Sum of quantity shares of the three largest suppliers.
- **Top-5 share**: Sum of quantity shares of the five largest suppliers.

## 8. Concentration metrics
- **HHI**: The Herfindahl-Hirschman Index is calculated as the sum of squared supplier quantity shares (`hhi_0_1`). Provided in both [0-1] and conventional [0-10,000] scale (`hhi_0_10000`).
- **Entropy**: Shannon entropy calculated as `-Σ(p_i × ln(p_i))`, where higher values indicate greater diversity.
- **Normalized entropy**: Entropy divided by `ln(N)`. For `N=1` (single supplier), normalized entropy is explicitly set to `0` to prevent division by zero and correctly indicate a lack of diversity.

## 9. Import-dependence methodology
A defensible import-dependence metric was successfully created using the FAO Food Balance Sheets (FBS).
- **Numerator**: Net Imports (`fbs_import_quantity` - `fbs_export_quantity`).
- **Denominator**: Total Domestic Supply (`domestic_supply`).
- **Interpretation**: Measures the fraction of a country's total physical domestic availability of a commodity that is sourced from foreign net imports. 

## 10. Nutrition exposure
Calorie and protein exposure can be consistently calculated.
- The `Grand Total` item from the FBS dataset was extracted for every country-year.
- The specific commodity's `Food supply (kcal/capita/day)` and `Protein supply quantity (g/capita/day)` are divided by the Grand Total equivalents to compute `calorie_share` and `protein_share`.

## 11. Missingness
- **Trade and Concentration metrics**: Missing for ~101 country-years where supplier count/shares are absent (true zeros in imports).
- **FBS metrics**: Missing for ~8,000-9,000 records out of ~18,000 total cross-sections due to countries not tracked in the FAO FBS, or specific commodities being completely unrecorded for some countries. These remain properly marked as `NaN` (not zero-filled).

## 12. Validation results
- **Check A (Country coverage)**: 220 universe expected. 178 present in trade data, 42 absent/no trade. PASS.
- **Check B (Commodity coverage)**: Exactly 6 commodities. PASS.
- **Check C (Year coverage)**: Exactly 14 years (2010-2023). PASS.
- **Check D (HHI)**: All HHI values strictly bounded between 0 and 1. PASS.
- **Check E (Supplier shares)**: For all positive-import records, shares sum to exactly 1. PASS.
- **Check F (Entropy)**: All entropy values ≥ 0. Normalized entropy bounded between 0 and 1. PASS.
- **Check G (Largest supplier)**: Largest share bounded between 0 and 1. PASS.
- **Check H (Top-3 and Top-5)**: Bounded between 0 and 1, and Top-5 ≥ Top-3 ≥ Largest. PASS.
- **Check I (Trade totals)**: Trade totals correctly reconcile with the Step 6A dataset. PASS.
- **Check J (FBS consistency)**: FBS data successfully mapped by M49 codes, item codes, and specific Elements. PASS.

## 13. Limitations
1. **FBS Imputation**: Import dependence uses total domestic supply as the denominator. This does not disentangle human food consumption from livestock feed. A high dependency on imported maize might expose the livestock sector rather than directly threatening human caloric supply.
2. **Missing FBS Data**: The FAO FBS does not cover all 220 countries/economies. Many smaller economies and territories lack domestic supply and calorie data, leaving their import dependence technically undefined.
3. **Calorie Equality**: National per capita averages ignore socio-economic inequalities in caloric distribution.

## 14. Final status
**READY**
