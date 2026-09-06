# FOODSHIELD STEP 5B: TRADE FLOW VALIDATION REPORT

## 1. Source Information
- Source file: `data/raw/Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv`
- Source row count: 50428180
- Filtered row count: 501416 (Import Quantity + Import Value records)
- Final analytical dataset row count: 250708

## 2. Coverage Metrics
- Number of reporters: 193
- Number of partners: 214
- Number of bilateral pairs: 13322
- Number of commodities: 6
- Number of trade-item representations: 7
- Year range: 1986 to 2023

## 3. Aggregate Totals
- Total trade value (1000 USD): 3,002,991,302.00
- Total trade quantity (tonnes): 9,673,346,022.27

## 4. Diagnostics
- Missing quantity: 0
- Missing value: 0
- Zero quantity: 24576
- Zero value: 34895
- Self-trade records (Reporter == Partner): 429
- Duplicate records at Trade-Item level: 0
- Duplicate records at Commodity level (due to Sugar items 162/163): 108

## 5. Methodological Decisions & Remarks
- **Import Direction:** Kept only 'Import quantity' and 'Import value' elements from FAOSTAT. They were merged on common keys so each row has a quantity and trade_value.
- **Missing/Zero:** Left them as NaN/0 instead of removing them to avoid losing other valid information in the same row.
- **Self-Trade:** Identified but not removed. Can be filtered out downstream if needed.
- **Sugar Aggregation:** Items 162 and 163 both map to Sugar. The dataset retains `trade_item_code` for auditability. Aggregating to Commodity level will require summing 162 and 163 where applicable.

