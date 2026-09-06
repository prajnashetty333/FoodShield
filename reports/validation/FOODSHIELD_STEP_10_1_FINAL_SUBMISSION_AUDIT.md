# FOODSHIELD Step 10.1 Final Submission Audit

**Audit date:** 2026-09-05  
**Scope:** Read-only audit of the locked Step 9I repository. No analytical input, methodology, or analytical output was regenerated or changed. This report is the sole audit artifact created.

## Verdict: PASS WITH FINDINGS

The locked analytical baseline reconciles exactly and the core methodology, policy framing, source data isolation, null serialization, and figure accounting are sound. The dashboard is broadly submission-ready, with one functional scope mismatch to resolve before final packaging: Replacement Pathway exposes Rank 2/3 selections despite serving Rank-1-only replacement data. The requested live backend/API/browser verification could not be performed in this environment because no Python interpreter is installed.

## Finding register

| Severity | Finding | Evidence and submission impact |
|---|---|---|
| **HIGH** | Replacement Pathway offers Rank 2/3 selections with no matching API data. | `ReplacementPathway.tsx` renders Rank 1, 2, and 3 selectors. `DataLoader.get_replacement_results()` filters the replacement CSV to `shock_rank == 1` before `replacement_service.py` filters the requested rank. Rank 2/3 requests therefore return 404. This also contradicts the page's implication that the selected rank has a modeled replacement pathway. |
| **HIGH** | Required runtime verification is not reproducible in this audit environment. | `py -3` reports no installed Python. Therefore FastAPI could not be started and `scripts/test_api.py`, live endpoint HTTP status checks, frontend routes through the API, and browser-console checks could not be independently run. The earlier Step 9I report's 15/15 result is historical evidence only, not this audit's verification. |
| **MEDIUM** | Production client payload is unnecessarily large. | `npm.cmd run build` succeeds, but emits a 4.44 MB minified JavaScript bundle (1.36 MB gzip), primarily consistent with bundled Plotly. It is not a large analytical CSV and does not invalidate the analysis, but it is a material dashboard-load warning. |
| **LOW** | Release hygiene contains obvious development residue and generic presentation metadata. | `scratch/test_sens.py`, `scratch/test_script.py`, `scratch/__pycache__/`, `frontend/src/counter.ts`, `assets/vite.svg`, `assets/typescript.svg`, and a generic document title `frontend` remain. No files were removed. |
| **LOW** | Build produces `frontend/dist/` (4,475,294 bytes) and reports future Vite `__dirname` compatibility plus chunk-size warnings. | The build itself passed. Confirm the packaging policy excludes/generated `dist` is not accidentally submitted unless intended. |

## 1. Source-of-truth trace

The trace is present and uses processed FOODSHIELD outputs:

`FAOSTAT raw trade/FBS` → `foodshield_trade_flows` → bilateral trade/country and commodity universes → exposure metrics and supplier shares → network/history → supplier shock scenarios → replacement candidates, allocations, results → resilience metrics/profiles/aggregates → sensitivity/research findings → policy documents/figures → FastAPI → React.

The live backend is configured only for `data/processed/foodshield/` CSVs:

| Dashboard function | API/service | Configured validated source and columns used |
|---|---|---|
| Executive Overview | `/api/overview` → `overview_service` | `resilience_metrics`: `replacement_rate`, `resilience_profile` |
| Country Explorer | `/api/countries/options`, `/analysis` → `country_service` | `resilience_metrics`: importer, commodity, year, exposure, loss, tier, rate, profile columns; code/name map from `supplier_shock`: importer code/name |
| Commodity Explorer | `/api/commodities`, `/analysis` → `commodity_service` | `resilience_metrics`: commodity, replacement/loss/HHI/profile columns |
| Supplier Shock | `/api/shocks/analysis` → `shock_service` | `supplier_shock`: importer, commodity, year, supplier rank/name, lost quantity, loss and remaining shares |
| Replacement Pathway | `/api/replacement/analysis` → `replacement_service` | `replacement_results`: rank, supplier, lost supply, Tiers 1–3, unreplaced, rate, new-origin share, outcome/capacity status |
| Sensitivity | `/api/sensitivity/analysis` → `sensitivity_service` | `sensitivity_summary`: experiment, mean replacement rate, Type-A share; `sensitivity_profile_transitions`: experiment, transition-count columns |
| Policy & Decision | `/api/policy` | Static conditional framework and disclaimer; no analytical calculation |
| Methodology | `/api/methodology` | Static limitations/disclaimer; no analytical calculation |

No API/backend module reads `data/raw`, and the React API client only requests API endpoints. The frontend formats/display plots but does not calculate analytical metrics. `DataLoader` caches each loaded CSV (`lru_cache(maxsize=1)`), so large analytical CSVs are not sent to the browser.

## 2. Locked baseline reconciliation — PASS

Independent PowerShell calculation directly from `foodshield_resilience_metrics_2010_2023.csv`, filtered to rank 1, 2011–2023, six locked commodities, and `capacity_available`:

| Metric | Independently calculated | Expected | Result |
|---|---:|---:|---|
| Scenarios | 10,953 | 10,953 | PASS |
| A / Existing-network resilient | 9,534 (87.0446%) | 9,534 (87.04%) | PASS |
| B / Historically recoverable | 438 (3.9989%) | 438 (4.00%) | PASS |
| C / New-origin dependent | 936 (8.5456%) | 936 (8.55%) | PASS |
| D / Structurally constrained | 45 (0.4108%) | 45 (0.41%) | PASS |
| Mean modeled replacement | 99.833013% | ≈99.83% | PASS |
| Mean shock-loss share | 67.170389% | ≈67.17% | PASS |

All six displayed commodities are exactly Wheat, Rice, Maize, Palm Oil, Sugar, and Sunflower Oil. The primary scope years are exactly 2011–2023.

## 3. Methodology and missing-data integrity — PASS

Code review confirms: Rank 1 is primary; Rank 2/3 shocks are independent in Supplier Shock; no cumulative shock implementation was found. Replacement classifies Tier 1 current-year suppliers, Tier 2 historically observed suppliers, then Tier 3 new origins, excludes both importer and shocked supplier, allocates sequentially, caps replacement at loss, and uses only pre-shock historical maxima. HEEC is calculated as `max(0, pre-shock historical max - current global outward trade)`; 2010 is explicitly capacity-history-insufficient; global outward trade includes the shocked supplier's other exports.

Profile definitions match A/B/C/D exactly. No domestic-production or commodity-substitution allocation exists. Sensitivity uses only 1.00/0.75/0.50/0.25 HEEC multipliers, leaves tier eligibility unchanged, retains the loss bound, and uses historical data before the shock year.

The 0.25 capacity-summary row independently gives 98.906379% mean modeled replacement and 79.978088% Type A, matching the expected ≈98.91% and ≈79.98%.

The backend serializes NaN/None as null through all `safe_float` functions; it does not coerce those API observations to zero. Search results found `fillna(0)` only in upstream calculation/validation/diagnostic contexts (e.g., a missing supplier count, comparison checks, and grouped diagnostic tables), not in backend API serialization. These should be retained as audit-visible implementation caveats, but no downstream dashboard missing-observation-to-zero conversion was found.

## 4. Figures — PASS

Figures 01–08 all exist, have substantive raster dimensions, and their catalog gives the stated source, scope, metric, denominator, units, and non-causal limitation. Figures 01/02/03/04/08 use the resilience metrics scope; Figure 05 uses the persistence dataset; Figure 07 uses transitions. Figure 03's independent reconciliation passes: for all 10,953 primary rows, `Tier 1 + Tier 2 + Tier 3 + unreplaced = lost supply` exactly (maximum numerical difference 0 tonnes).

The labels and limitations appropriately say modeled replacement/HEEC proxy and avoid causal claims. Figure 06's stated source and metrics reconcile: the sensitivity-summary header contains both `mean_replacement_rate` and `type_A_share`.

## 5. Claims, country/commodity, policy, documentation — PASS

Searches of README, reports, frontend, and backend found the requested terms only in disclaimers, limitations, questions, or explicit prohibited-claim examples. No unsupported positive claim was found. The wording consistently frames FOODSHIELD as decision support, modeled supplier-shock loss/modeled replacement, HEEC proxy, and not a forecast, causal conclusion, or guarantee of real-world food security.

Country display names are dynamically derived from the validated supplier-shock CSV while FAO codes remain the join keys. No hardcoded country list exists. Sugar is aggregated in the shock/bilateral pipeline by commodity after the two validated trade representations, preserving the documented anti-double-counting treatment.

Policy guidance is conditional and maps A→maintain/monitor, B→preserve/revive historical relationships, C→develop/qualify additional origins, and D→investigate constraints/contingencies. It explicitly disclaims prediction, causality, and guarantees.

README, narrative, judge Q&A, figure map, policy documents, and validation reports agree with the locked baseline values and framing.

## 6. Build, API, routes, performance, and hygiene

`npm.cmd run build` completed successfully: TypeScript and Vite both passed. It generated the `dist` files noted above and emitted warnings, not errors. Python-dependent backend tests and live API/browser console checks were not runnable because the environment lacks Python; this audit does not represent them as passing.

Performance architecture is otherwise appropriate: the browser receives compact API responses, the backend caches loaded CSVs, and the React pages do not load/process the large source CSVs. The bundle-size warning is a release-performance concern, not a data-flow failure.

No plaintext credential pattern was found outside data, and `.gitignore` covers environment files, Python bytecode, raw/processed data, and output folders. Git inspection itself was unavailable because the workspace's Git metadata points at an inaccessible `C:/Users/prajn` path; repository tracked/untracked status cannot be independently certified here.

## Required disposition before packaging

Before final packaging, resolve the Rank 2/3 Replacement Pathway exposure and regression-test it in an environment with Python. Re-run all API HTTP/error-route tests and browser route/console checks. This audit makes no claim that any finding has been fixed and does not declare Step 10 complete.

## Post-audit verification record — 2026-09-05

The Replacement Pathway presentation-scope fix was reviewed after this audit report was issued.

| Check | Result | Evidence |
|---|---|---|
| Replacement Pathway Rank scope | PASS (static) | `ReplacementPathway.tsx` fixes `PRIMARY_SHOCK_RANK = 1`, makes the only displayed value `Rank 1 (Primary)`, and calls `fetchReplacementAnalysis` only with that constant. No Rank-2/Rank-3 replacement UI path remains. |
| Supplier Shock rank scope | PASS (static) | `SupplierShock.tsx` retains Rank 1, 2, and 3 selections and its independent-shock explanatory note. |
| Primary replacement accounting | PASS | Direct CSV check: 10,953 primary rows and zero non-reconciling rows for `Tier 1 + Tier 2 + Tier 3 + Unreplaced = Lost Supply`. |
| Frontend build | PASS | `npm.cmd run build` completed with TypeScript/Vite success; existing Vite compatibility and bundle-size warnings remain. |
| API HTTP tests, invalid-route tests, live rank requests | NOT RUN | `py -3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000` cannot start because the Python launcher reports no installed Python runtime. |
| Eight browser routes and console | NOT RUN | No browser surface is available in this session, and the backend could not be started. |
| Analytical CSV integrity | PASS (current-state hash) | SHA-256: replacement results `C7E268B9905EC78C56BCCC9150A0F80673870D5C1F7E3929C5A0C4DCEC27D5D4`; resilience metrics `A753D39096BD247D20BDAF07E5ABFC34D609B90799ECECA7221F5A5A86A21BA9`; sensitivity summary `4CF539B9876D5524062D7666CA744842EAF47E3C38BD334B43EDC53D1CA7BE24`; supplier shock `C77B6F9638A0A3F600F9194E4CB2ECF3B5AA11D8642EA449EF6026C2451114B1`. |

This record does not declare Step 10.1 PASS or Step 10 complete. The remaining required verification is live backend/API/browser testing in a Python-enabled environment.
