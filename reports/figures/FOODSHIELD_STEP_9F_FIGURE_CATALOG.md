# FOODSHIELD STEP 9F - FIGURE CATALOG

## Figure 01
**Filename:** fig01_supplier_concentration.png
**Research Question:** How concentrated are food imports among suppliers before the shock?
**Source Dataset:** foodshield_resilience_metrics_2010_2023.csv
**Exact Metric(s):** largest_supplier_share
**Population/Scope:** Rank 1, 2011–2023, capacity-valid, 6 commodities
**Aggregation Method:** Distribution shown as boxplots by commodity
**Denominator:** N/A (share is of total imports)
**Interpretation:** Shows the baseline exposure by commodity to the loss of a single largest supplier.
**Important Limitation:** Concentration alone does not determine replacement capacity or resilience.

## Figure 02
**Filename:** fig02_shock_severity_by_commodity.png
**Research Question:** How large is the modeled loss when the largest supplier disappears?
**Source Dataset:** foodshield_resilience_metrics_2010_2023.csv
**Exact Metric(s):** shock_loss_share
**Population/Scope:** Rank 1, 2011–2023, capacity-valid, 6 commodities
**Aggregation Method:** Mean shock loss share per commodity
**Denominator:** Baseline imports
**Interpretation:** Visualizes the immediate volume of supply lost on average due to the modeled Rank-1 shock.
**Important Limitation:** Represents an instantaneous loss assumption without accounting for domestic adaptation or policy responses.

## Figure 03
**Filename:** fig03_replacement_pathway_by_commodity.png
**Research Question:** When a major supplier disappears, where does replacement come from?
**Source Dataset:** foodshield_resilience_metrics_2010_2023.csv
**Exact Metric(s):** tier1_replacement, tier2_replacement, tier3_replacement, unreplaced_supply
**Population/Scope:** Rank 1, 2011–2023, capacity-valid, 6 commodities
**Aggregation Method:** Sum of replacements and unreplaced supply by commodity
**Denominator:** Total lost supply
**Interpretation:** Shows where modeled replacement comes from. Most replacement is drawn from existing connected suppliers.
**Important Limitation:** Historical trade expansion capacity is a proxy and does not guarantee future physical availability.

## Figure 04
**Filename:** fig04_resilience_profiles.png
**Research Question:** What proportion of modeled supplier shocks fall into each recovery pathway?
**Source Dataset:** foodshield_resilience_metrics_2010_2023.csv
**Exact Metric(s):** resilience_profile
**Population/Scope:** Rank 1, 2011–2023, capacity-valid, 6 commodities
**Aggregation Method:** Percentage of scenarios in each profile
**Denominator:** Total number of modeled scenarios
**Interpretation:** Demonstrates that while most shocks are resolved by existing suppliers, a fraction requires structurally difficult pathways (historical or new origins).
**Important Limitation:** Replacement rate approaches 100% does NOT mean the country's food supply is fully secure, only mathematically replaceable under model assumptions.

## Figure 05
**Filename:** fig05_persistent_constraints_heatmap.png
**Research Question:** Which country–commodity systems repeatedly experience difficult replacement pathways?
**Source Dataset:** foodshield_resilience_country_commodity_persistence_2010_2023.csv
**Exact Metric(s):** resilience_profile over time for systems with repeated_type_c or repeated_type_d
**Population/Scope:** Country-commodity systems with persistent Type C/D behavior
**Aggregation Method:** Heatmap of profile per year (top 40 by severity sort)
**Denominator:** N/A
**Interpretation:** Highlights structural vulnerabilities where particular importers repeatedly lack existing supply networks to replace their main supplier.
**Important Limitation:** Based entirely on historical trade data and does not incorporate geopolitical or internal policy factors.

## Figure 06
**Filename:** fig06_capacity_sensitivity.png
**Research Question:** How sensitive are replacement outcomes to the assumed historical export-expansion capacity?
**Source Dataset:** foodshield_sensitivity_summary_2010_2023.csv
**Exact Metric(s):** mean_replacement_rate, type_A_share
**Population/Scope:** Rank 1, 2011–2023, capacity-valid across capacity multipliers (1.0, 0.75, 0.5, 0.25)
**Aggregation Method:** Mean rate and share across all valid scenarios per multiplier
**Denominator:** Total lost supply (for rate), Total scenarios (for share)
**Interpretation:** As assumed expansion capacity shrinks, overall replacement remains robust but reliance on existing suppliers (Type A) declines.
**Important Limitation:** HEEC is a historical proxy, and scaling it downwards provides a stress test rather than a forecast.

## Figure 07
**Filename:** fig07_profile_transition_heatmap.png
**Research Question:** When capacity assumptions become more restrictive, how do recovery pathways change?
**Source Dataset:** foodshield_sensitivity_profile_transitions_2010_2023.csv
**Exact Metric(s):** Profile transition counts (A_to_A, A_to_B, etc.)
**Population/Scope:** Scenarios compared between 1.00 HEEC and 0.25 HEEC
**Aggregation Method:** Count of scenarios transitioning between profiles
**Denominator:** N/A (raw counts)
**Interpretation:** Lower capacity assumptions shift modeled scenarios toward pathways requiring historical suppliers, new origins, or incomplete replacement.
**Important Limitation:** Transitions reflect mathematical capacity limits, not behavioral responses of countries under duress.

## Figure 08
**Filename:** fig08_exposure_vs_replacement.png
**Research Question:** Is higher supplier concentration visibly associated with lower modeled replacement?
**Source Dataset:** foodshield_resilience_metrics_2010_2023.csv
**Exact Metric(s):** largest_supplier_share, replacement_rate, lost_supply
**Population/Scope:** Rank 1, 2011–2023, capacity-valid, 6 commodities
**Aggregation Method:** Scatter plot, bubble size scaled by lost_supply
**Denominator:** Baseline imports (for concentration), Lost supply (for replacement rate)
**Interpretation:** Explores the descriptive association between baseline exposure and recovery success.
**Important Limitation:** Descriptive association only; this figure does not establish causality.
