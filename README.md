# FOODSHIELD — Food Trade Resilience

FOODSHIELD is a DataThon research project evaluating historical food-import exposure and counterfactual supplier-shock replacement feasibility. It is decision support: modeled replacement is not a forecast or guarantee of real-world food security.

## Research question and scope

When a supplier disappears, how much modeled lost supply can be replaced through current suppliers, historically observed suppliers, and qualifying new origins under the Historical Export-Expansion Capacity (HEEC) proxy?

- Primary capacity-valid scope: 2011–2023; source period: 2010–2023.
- Locked commodities: Wheat, Rice, Maize, Palm Oil, Sugar, and Sunflower Oil. Sugar uses its two validated trade representations.
- Countries: `data/processed/foodshield/foodshield_country_universe.csv`.
- Primary replacement: independent Rank-1 shock. Supplier Shock separately presents independent Rank 1/2/3 shocks.

## Analytical pipeline

`FAOSTAT → Data Engineering → Country × Commodity Dataset → Exposure Analysis → Supplier Network → Supplier Shock → Replacement Engine → Resilience Profiles → Sensitivity Analysis → Evidence Synthesis → Policy Insights → Dashboard`

Tier 1 is current-year suppliers, Tier 2 historically observed suppliers, and Tier 3 new origins. HEEC is a historical export-expansion proxy, not observed spare physical capacity.

## Repository guide

| Area | Purpose |
|---|---|
| `data/raw/` | FAOSTAT source data |
| `data/processed/foodshield/` | locked and derived analytical outputs |
| `src/` | reproducible pipeline code by stage |
| `backend/` | FastAPI API and cached read-only data services |
| `frontend/` | React dashboard |
| `reports/` | methodology, validation, figures, and policy outputs |
| `scripts/` | operational validation scripts |
| `scratch/` | retained development experiments; not production inputs |

See [project map](docs/PROJECT_MAP.md), [file status](docs/FILE_STATUS.md), [runbook](docs/RUNBOOK.md), and [change policy](docs/CHANGE_POLICY.md).

## Run locally

Backend requires Python and packages in `requirements.txt`:

```powershell
py -3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Use `npm run build` to build the frontend. Do not casually run pipeline scripts: they can overwrite locked outputs.

Production hosting (Render backend, Vercel frontend) is documented in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). The API is `backend.main:app` and must be started from the repository root.

## Status and limitations

The locked primary baseline has 10,953 scenarios and 99.83% mean modeled replacement. Current validation is recorded in `reports/validation/FOODSHIELD_STEP_10_1_FINAL_SUBMISSION_AUDIT.md`; live FastAPI/browser verification remains environment-dependent.

FOODSHIELD does not model future availability, prices, logistics, contracts, policy response, domestic production adaptation, commodity substitution, or consumer-level food security, and does not establish causality.
