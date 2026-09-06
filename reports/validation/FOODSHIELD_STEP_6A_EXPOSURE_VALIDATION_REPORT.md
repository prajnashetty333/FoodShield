# FOODSHIELD STEP 6A: EXPOSURE VALIDATION REPORT

## 1. Analytical Period
- Min Year: 2010
- Max Year: 2023
- Number of Years: 14 (Expected 14)

## 2. Country Coverage
- Expected countries/economies: 220
- Countries appearing in trade: 198
- Countries with no trade observations: 22

## 3. Commodity Coverage
- Number of commodities: 6
- Commodities: Sugar, Sunflower Oil, Wheat, Maize, Palm Oil, Rice

## 4. Observations
- Country × Commodity × Year (Exposure): 11799
- Bilateral Supplier (Country × Supplier × Commodity × Year): 138436

## 5. Aggregate Totals
- Sugar: Quantity = 409,324,399.25 tonnes, Value = 198,327,981.00 kUSD
- Sunflower Oil: Quantity = 140,430,529.29 tonnes, Value = 153,952,924.00 kUSD
- Wheat: Quantity = 2,033,883,617.71 tonnes, Value = 592,366,364.00 kUSD
- Maize: Quantity = 1,963,055,342.19 tonnes, Value = 530,088,843.00 kUSD
- Palm Oil: Quantity = 541,905,083.16 tonnes, Value = 470,689,008.00 kUSD
- Rice: Quantity = 35,799,283.67 tonnes, Value = 15,572,450.00 kUSD

## 6. Supplier-count statistics
- Average suppliers per country-commodity-year: 10.89
- Median suppliers per country-commodity-year: 8.0
- Max suppliers per country-commodity-year: 79

## 7. Diagnostics
- Missing import quantities: 0
- Zero import quantities: 9950
- Negative import quantities: 0
- Negative import values: 0
- Self-trade records identified and excluded from bilateral: 80 (Qty: 46,988)
- Duplicate records in Bilateral dataset: 0
- Duplicate records in Exposure dataset: 0

## 8. Validations
- **Sugar Aggregation**: Validated. Items 162 and 163 grouped by commodity='Sugar'. Trade item codes tracked in audit columns.
- **Supplier Share Validation**: Validated. Shares sum to 1 (Max Qty Deviation: 2.22e-16, Max Val Deviation: 2.22e-16).

## 9. Methodological Decisions & Limitations
- **Self-trade**: Excluded from the network/supplier layers to correctly represent external risk.
- **Negative Values**: None found (if >0). Should verify manually if any exist.
- **Limitations**: Zero or missing quantities imply structural missingness or true zero, handled identically in volume calculations but distinguishable in missingness flags if necessary downstream.

## 10. Final Status
Step 6A is complete and ready for the next stage.
