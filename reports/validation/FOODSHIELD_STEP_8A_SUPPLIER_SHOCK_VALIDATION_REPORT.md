# FOODSHIELD STEP 8A: SUPPLIER SHOCK ENGINE - VALIDATION REPORT

## 1. Objective
Build a reproducible supplier-disappearance shock engine to simulate the immediate supply loss if a foreign supplier disappears, using the historical bilateral supplier network.

## 2. Methodology
The historical bilateral trade network was aggregated by Importer × Commodity × Year × Supplier. Self-trade was excluded. Suppliers were ranked by descending import quantity (with supplier country code as deterministic tie-breaker).

## 3. Shock Definition
For every supplier, we simulate their disappearance:
- `baseline_imports(C,F,Y)` = sum of all positive supplier import quantities
- `lost_supply(C,F,Y,S)` = `import_quantity(C,S,F,Y)`
- `shocked_imports(C,F,Y,S)` = `baseline_imports(C,F,Y)` - `lost_supply(C,F,Y,S)`
- `shock_loss_share(C,F,Y,S)` = `lost_supply` / `baseline_imports`
- `remaining_import_share` = 1 - `shock_loss_share`

## 4. Mathematical Formulas
See above Section 3.

## 5. Input Datasets
- `data/processed/foodshield/foodshield_bilateral_trade_2010_2023.csv`
- `data/processed/foodshield/foodshield_exposure_metrics_2010_2023.csv`

## 6. Number of importer-commodity-year observations
11698

## 7. Number of supplier shock observations
128486

## 8. Number of Rank 1 scenarios
11698

## 9. Number of Rank 2 scenarios
11043

## 10. Number of Rank 3 scenarios
10323

## 11. Number of single-supplier cases
655

## 12. Number of two-supplier cases
720

## 13. Average Rank 1 shock loss
0.6720

## 14. Median Rank 1 shock loss
0.6607

## 15. Maximum Rank 1 shock loss
1.0000

## 16. Commodity-level shock statistics
Average Rank 1 shock loss by commodity:
{'Maize': 0.6681232333814967, 'Palm Oil': 0.6505928737312068, 'Rice': 0.7779809162156236, 'Sugar': 0.6822070380688773, 'Sunflower Oil': 0.6199705809035531, 'Wheat': 0.6429274865713231}

## 17. Country-level shock statistics
Overall shock statistics summarized in outputs. Average Rank 1 loss across all countries is 0.6720.

## 18. Validation Results
- CHECK 1: sum supplier quantities = baseline imports: PASS
- CHECK 2: Supplier shares sum to ~1: PASS
- CHECK 3: shocked_imports = baseline - lost_supply: PASS
- CHECK 4: remaining_import_share = 1 - shock_loss_share: PASS
- CHECK 5: Rank 1 equals largest supplier by quantity: PASS
- CHECK 6: Rank 2 quantity <= Rank 1 quantity: PASS
- CHECK 7: Rank 3 quantity <= Rank 2 quantity: PASS
- CHECK 8: shock_loss_share between 0 and 1: PASS
- CHECK 9: remaining_import_share between 0 and 1: PASS
- CHECK 10: No self-trade edges: PASS
- CHECK 11: Only locked commodities appear: PASS
- CHECK 12: Years 2010-2023: PASS
- CHECK 13: No duplicate analytical keys: PASS
- CHECK 14: Rank 1 share equals STEP 7A largest_supplier_share: PASS
- CHECK 15: Reconcile baseline imports with STEP 7: PASS

## 19. Edge Cases
- Single-supplier cases mapped to rank 1, shock loss 1.0, remaining 0.
- Missing values for quantity were ignored (only positive flows used).
- Self-trade was excluded.
- Sugar representations aggregated.

## 20. Limitations
- Values assume no immediate substitution or replacement supply (to be addressed in Step 8B).
- Missing quantities are not imputed.

## 21. Methodological Decisions
- Quantity is the primary shock measure.
- Supplier code used as deterministic tie-breaker for ranks.

## 22. Final PASS/FAIL status
PASS

### WHAT WE DID
- Ingested bilateral trade data and locked exposure metrics.
- Excluded self-trade and filtered to positive quantities.
- Aggregated duplicate commodity representations (Sugar).
- Ranked suppliers by quantity and computed shock metrics (Rank 1, 2, 3, etc.).
- Generated detailed shock dataset, standard scenarios, and summary tables.
- Validated inputs and logic with 15 rigorous checks.

### WHAT WE DO NEXT
- Explain that STEP 8B will build the Replacement Engine.
