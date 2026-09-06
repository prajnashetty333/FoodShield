# FOODSHIELD_STEP_8B_REPLACEMENT_VALIDATION_REPORT

## Executive Summary
Step 8B measures replacement feasibility for Rank-1 supplier shocks across 2010-2023 for six locked commodities. It assesses whether existing, historical, or new origin suppliers have sufficient capacity to replace lost supply.

## Methodology
- **Rank-1 shock**: The largest supplier to an importer is removed.
- **Tier 1**: Existing current suppliers (quantity > 0 in shock year).
- **Tier 2**: Historical suppliers (quantity > 0 in >= 2 pre-shock years, 0 in shock year).
- **Tier 3**: New origins (eligible capacity, no qualifying bilateral relationship).
- **HEEC**: max(0, historical_pre_shock_max - current_year_global_outward_trade).
- **Allocation**: Sequential by tier, proportional by HEEC within tier.
- **2010 Treatment**: No pre-shock history exists, marked `capacity_history_insufficient`.
- **Outcome Classification**: A (Tier 1 suffices), B (Tier 1+2 suffices), C (Tier 1+2+3 suffices), D (Structurally unreplaced).

## Dataset Statistics
- Scenarios: 11698
- Candidate rows: 1889173
- Allocation rows: 172100
- Importer count: 178
- Commodity count: 6
- Year range: 2010-2023
- Tier 1 candidate count: 111027
- Tier 2 candidate count: 41442
- Tier 3 candidate count: 1736704

## Replacement Statistics
- Mean replacement rate: 0.9983
- Median replacement rate: 1.0000
- Type A share: 87.04%
- Type B share: 4.00%
- Type C share: 8.55%
- Type D share: 0.41%
- Mean Tier 1 replacement: 227093.98
- Mean Tier 2 replacement: 7535.71
- Mean Tier 3 replacement: 15395.89
- Mean new-origin share: 0.0731
- Unreplaced supply: 66953055.24

## HEEC Diagnostics
- Number of capacity-valid scenarios: 10953
- Number of insufficient-history scenarios: 745
- Number of candidates with zero HEEC: 572303

## Validation
1. PASS
2. PASS
3. PASS
4. PASS
5. PASS
6. PASS
7. PASS
8. PASS
9. PASS
10. PASS
11. PASS
12. PASS
13. PASS
14. PASS
15. PASS
16. PASS
17. PASS
18. PASS
19. PASS
20. PASS
21. PASS
22. PASS
23. PASS
24. PASS

## Limitations
1. HEEC is a historical trade-expansion proxy, not observed spare physical capacity.
2. Bilateral quantities are based on the approved FAOSTAT trade-flow representation.
3. The model does not observe contracts, inventories, shipping constraints, tariffs, political restrictions, or real-time exporter capacity.
4. Domestic production adaptation is excluded.
5. Commodity substitution is excluded.
6. Trade friction is represented through relationship tiers rather than explicit cost variables.
7. 2010 cannot receive a primary capacity-constrained estimate because no pre-2010 history exists.
8. Independent Rank-2/Rank-3 shocks are sensitivity scenarios, not cumulative shocks.
9. Replacement feasibility should not be called "resilience" until the dedicated resilience layer is implemented.
