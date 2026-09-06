# FOODSHIELD STEP 5A: Trade Matrix Schema & Data Foundation Audit

## A. Exact Trade-Matrix Schema
Columns present in `Trade_DetailedTradeMatrix_E_All_Data_(Normalized).csv`:
- `Reporter Country Code`
- `Reporter Country Code (M49)`
- `Reporter Countries`
- `Partner Country Code`
- `Partner Country Code (M49)`
- `Partner Countries`
- `Item Code`
- `Item Code (CPC)`
- `Item`
- `Element Code`
- `Element`
- `Year Code`
- `Year`
- `Unit`
- `Value`
- `Flag`

## B. Exact Filtering Strategy Recommended for Step 5B
- **Elements**: Filter to `Export Quantity` (and `Import Quantity` if verifying mirror flows) to determine physical trade volumes. Use `Export Value` / `Import Value` if financial metrics are needed.
- **Commodities**: Filter `Item Code` to the 6 validated trade item codes.
- **Countries**: Filter both `Reporter Country Code` and `Partner Country Code` to the 220 validated country codes to ensure strict bilateral valid country flows.

## C. Commodity Matching Results
| Commodity | Expected CPC | Found in Trade Matrix? | Trade Item Code | Trade Item Name | Notes |
|---|---|---|---|---|---|
| Wheat | '0111 | Yes | 15 | Wheat | |
| Rice | '0113 | Yes | 27 | Rice | |
| Maize | '0112 | Yes | 56 | Maize (corn) | |
| Palm Oil | '2165 | Yes | 257 | Palm oil | |
| Sugar | '2351f | Yes | 162 | Raw cane or beet sugar (centrifugal only) | |
| Sugar | '23511.02 | Yes | 163 | Cane sugar, non-centrifugal | |
| Sunflower Oil | '21631.01 | Yes | 268 | Sunflower-seed oil, crude | |

## D. Country Matching Results
- Matched Reporter Entities: 193
- Unmatched Reporter Entities: 0
- Matched Partner Entities: 220
- Unmatched Partner Entities: 0

### Aggregate/Unmatched Entities (Examples)
These entities appear in the raw data but will be dropped during bilateral country filtering:
- Reporter Aggregates: []...
- Partner Aggregates: []...

## E. Duplicate Diagnostics
- Duplicate analytical keys (Reporter x Partner x Item x Element x Year) in filtered dataset: 0

## F. Estimated Filtered Dataset Size
- Original Rows: 50,428,180
- Filtered Rows: 983,090
- Size Reduction: Filtering reduces the dataset to approximately 1.95% of original rows.

## G. Methodological Decisions & Next Steps
1. **Data Direction**: FAOSTAT provides Imports and Exports. We should primary use Exports for exposure, and Imports for cross-validation if desired.
2. **Units**: Quantity is in tonnes (`t`). Value is in `1000 USD`.
3. **Aggregate Removal**: By strictly filtering reporters and partners to the 220 `country_code` universe, we perfectly drop regions (e.g. 'World', 'Africa') and invalid aggregates.

## H. WHAT WE DID / WHAT WE DO NEXT
**What we did**:
- Streamed 7.6GB dataset to identify the schema, commodity/country mapping logic, and row retention rates.
- Confirmed the validity of the 6 lock commodities against the data.
- Confirmed the country universe acts as an effective aggregate filter.

**What we do next**:
STEP 5B: BUILD THE FILTERED BILATERAL TRADE FLOW DATASET.
