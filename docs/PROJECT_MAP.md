# FOODSHIELD Project Map

FOODSHIELD analyzes historical import exposure and modeled supplier-shock replacement. Raw FAOSTAT files are in `data/raw/`; generated analytical files are in `data/processed/foodshield/` and are locked.

| Stage | Code | Input | Output | Status |
|---|---|---|---|---|
| Trade flows | `src/exposure/build_foodshield_trade_flows.py` | raw trade matrix, country universe | `foodshield_trade_flows.csv` | locked |
| Exposure | `src/exposure/build_foodshield_exposure.py`, `step7a_metrics.py` | trade flows, FBS | bilateral/exposure metrics | locked |
| Network | `src/network/step7b_network.py` | bilateral, exposure, universe | network/history | locked |
| Shock | `src/shock/step8a_supplier_shock.py` | bilateral, exposure | supplier shock/scenarios | locked |
| Replacement | `src/replacement/step8b_replacement.py` | bilateral, scenarios | candidates/allocation/results | locked |
| Resilience | `src/analysis/step9a_resilience_metrics.py` | replacement results | resilience metrics/profiles | locked |
| Synthesis | `step9c_resilience_aggregation.py`, `step9d_robustness_sensitivity.py`, `step9e_research_synthesis.py` | resilience/replacement data | aggregates, sensitivity, findings | locked |
| Figures | `src/visualization/step9f_visualizations.py` | locked summaries | `reports/figures/` | locked |
| Dashboard | `backend/`, `frontend/` | validated CSV API responses | interactive presentation | active |

Validations are in `reports/validation/`; methodology and presentation materials are in `reports/methodology/`; policy materials are in `reports/policy/`.
