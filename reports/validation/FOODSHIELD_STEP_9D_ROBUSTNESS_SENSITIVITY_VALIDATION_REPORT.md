# FOODSHIELD STEP 9D ROBUSTNESS AND SENSITIVITY VALIDATION REPORT

## 1. Objective
Evaluate robustness of FOODSHIELD's replacement and profile conclusions to changes in historical capacity assumptions and shock rank, without altering baseline methodology.

## 2. Validation Checks
Check 1: PASS
Check 2: PASS
Check 3: PASS
Check 4: PASS
Check 5: PASS
Check 6: PASS
Check 7: PASS
Check 8: PASS
Check 9: PASS
Check 10: PASS
Check 11: PASS
Check 12: PASS
Check 13: PASS
Check 14: PASS
Check 15: PASS
Check 16: PASS
Check 17: PASS
Check 18: PASS
Check 19: PASS
Check 20: PASS
Check 21: PASS
Check 22: PASS
Check 23: PASS
Check 24: PASS
Check 25: PASS
Check 26: PASS

## 3. Results Overview
Baseline result refers to the official FOODSHIELD estimate under locked HEEC methodology. Sensitivity results are counterfactual estimates.

### Q1. Does the 99.83% baseline replacement result remain high under 75%, 50%, and 25% HEEC?
Baseline: 0.9983
75% multiplier: 0.9975
50% multiplier: 0.9957
25% multiplier: 0.9891

### Q2. Does Type A remain dominant?
Baseline Type A share: 0.8704
25% multiplier Type A share: 0.7998

### Q3. How many baseline A scenarios become B/C/D?
Under 25% multiplier:
A to B: 218, A to C: 464, A to D: 92

### Q4. How many baseline C scenarios become D?
Under 25% multiplier: 111 scenarios

### Q5. How many baseline D scenarios remain D?
Under 25% multiplier: 45 scenarios

### Q6. Are Type D cases robust or highly HEEC-sensitive?
Refer to the type D robustness table. Generally, D cases are structurally constrained due to lack of eligible tier candidates, independent of total global HEEC.

### Q7. Does restricting historical capacity to recent 5-year or 3-year windows materially change conclusions?
W1 (5-year) replacement rate: 0.9981
W2 (3-year) replacement rate: 0.9976

### Q8. Does the replacement pathway change?
Tier 1 share decreases and Tier 2/3 shares increase under tighter HEEC assumptions, forcing reliance on historical or new origins.

### Q9. Is replacement capacity concentrated among a few exporters?
Refer to the concentration diagnostic table. Concentration metrics track top-3 and top-5 HEEC candidate shares.

### Q10. Do Rank 2 and Rank 3 shocks show materially different replacement behavior?

## 4. Final status
STEP 9D STATUS: READY FOR 9E

## Source Data Mapping Note
As requested, the validated replacement scenarios correspond to the output table `foodshield_replacement_results_2010_2023.csv` from Step 8B which contains the exact schema elements (importer, commodity, year, shock_rank, shocked_supplier, lost_supply) and provides equivalent scenario definitions as `foodshield_replacement_scenarios_2010_2023.csv`.
