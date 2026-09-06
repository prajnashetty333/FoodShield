# FOODSHIELD STEP 9E RESEARCH FINDINGS

## 1. Research Question
**When a country depends on one foreign supplier for an important food, can existing trade relationships replace most of the lost supply — or does resilience require a new origin?**

## 2. Analytical Scope
- **Commodities:** Wheat, Rice, Maize, Palm Oil, Sugar, Sunflower Oil.
- **Years:** 2011–2023 (Capacity-valid window).
- **Primary Shock:** Disappearance of the Rank-1 largest supplier.
- **Unit of Analysis:** Importer × Commodity × Year.
- **Capacity Assumption:** Baseline Historical Export-Expansion Capacity (HEEC).
- **Total Valid Scenarios:** 10,953

## 3. Evidence Chain

### 3.1 Exposure
Analysis of trade networks reveals substantial concentration. Many countries rely heavily on a single supplier for core commodities, creating significant structural exposure to supplier-specific shocks.

### 3.2 Supplier Shock
When a country's largest supplier disappears, the resulting supply loss is severe.
- **Mean Loss:** 67.17% of baseline imports.
- **Median Loss:** 66.10%.
- **Maximum Loss:** 100%.
*(Note: This represents the loss caused by the disappearance of the largest supplier, not total domestic food insecurity.)*

### 3.3 Replacement Feasibility
Despite the severity of Rank-1 shocks, the global network demonstrates high replacement capability under historical capacity constraints.
- **Mean Replacement Rate:** 0.9983 (or 99.83%).
This indicates that 99.83% of modeled Rank-1 supplier-shock losses are replaced on average under the historical trade-expansion capacity proxy.

### 3.4 Replacement Pathways
Replacement pathways fall into four validated resilience profiles:
- **Type A (Existing-network resilient):** 9,534 scenarios (87.04%). Current-year existing suppliers can fully replace the lost supply.
- **Type B (Historically recoverable):** 438 scenarios (4.00%). Current suppliers alone are insufficient, but historically observed suppliers can complete replacement.
- **Type C (New-origin dependent):** 936 scenarios (8.55%). Current and historical suppliers are insufficient, so a new origin is required.
- **Type D (Structurally constrained):** 45 scenarios (0.41%). Even the modeled Tier 3 pool cannot fully replace the lost supply.

### 3.5 Persistent Constraints
- **Repeated Type C Systems:** 224 country-commodity pairs repeatedly exhibited dependence on new origins.
- **Repeated Type D Systems:** 9 systems exhibited recurring modeled structural constraints.

### 3.6 Robustness
When global available replacement capacity (HEEC) is reduced by 75% (Multiplier 0.25):
- The overall mean replacement rate drops slightly to 0.9891.
- The share of Type A profiles falls to 79.98%.
- 464 baseline Type A cases become Type C, and 111 Type C cases downgrade to Type D.
Shortening the historical lookback window to 5 years (W1) yields a replacement rate of 0.9981, and 3 years (W2) yields 0.9976. The core conclusion remains materially unchanged.

## 4. Core Findings
1. High baseline replacement capability exists under the HEEC proxy.
2. The vast majority of Rank-1 shocks can be resolved using existing (Type A) networks.
3. A small but critical subset of shocks requires historically observed (Type B) or entirely new (Type C) trade origins.
4. Very few cases are completely unreplaceable (Type D) globally, pointing to localized tier-connectivity limits rather than a global lack of volume.

## 5. Commodity Findings
Detailed metrics per commodity are available in `foodshield_commodity_findings_2010_2023.csv`.

## 6. Country Findings
Detailed metrics per country are available in `foodshield_country_findings_2010_2023.csv`.

## 7. Persistent Country–Commodity Systems
Detailed records of recursively constrained country systems are available in `foodshield_persistent_systems_2010_2023.csv`.

## 8. Robustness Findings
Robustness testing confirmed that while restricting capacity pushes more countries to rely on historical or new origins, the overall system replacement rate remains extremely high (above 98%) even when 75% of global HEEC is wiped out.

## 9. Answer to the Research Question
Most modeled Rank-1 supplier shocks can be absorbed through existing supplier networks under the baseline historical export-expansion capacity proxy. However, a meaningful minority require historically observed suppliers or genuinely new origins, while a small set remain structurally constrained. These conclusions remain broadly robust when HEEC capacity is substantially reduced or the historical window is shortened, although tighter capacity assumptions increase the number of cases requiring historical or new-origin replacement.

## 10. What the Results Do NOT Show
The model does NOT establish:
- actual future food availability
- guaranteed physical spare capacity
- prices
- transportation costs
- trade policy feasibility
- geopolitical feasibility
- contracts
- infrastructure constraints
- quality/specification compatibility beyond the locked commodity mapping
- domestic substitution
- dietary substitution
- consumer-level food insecurity
- causality
- future supplier behavior

HEEC is strictly a **historical export-expansion capacity proxy**.

## 11. Methodological Limitations
The analysis relies heavily on historical data to parameterize replacement capacity. Zero-filling was avoided for structural integrity, and no predictive or machine-learning methodologies were introduced. 

## 12. Evidence Boundaries
All statistics apply only to the explicitly modeled subset of six commodities across the specified country universe between 2011 and 2023.

## 13. Validation Summary
All 26 checks successfully passed, preventing data drift, maintaining methodological locks, and avoiding the introduction of composite scores or predictive layers.

## 14. Conclusion
The FOODSHIELD modeling pipeline has successfully reached Evidence Synthesis. The data indicates strong structural resilience in global food trade networks at the macro volume level, with localized vulnerabilities distinctly characterized through the resilience profiling system.
