# Repository Cleanup Report

**Date:** 2026-09-05  
**Status:** READY WITH WARNINGS

## Before

The repository already separated analytical stages, dashboard code, and reports, but its root README described only early pipeline work. The frontend retained an unreferenced Vite starter entrypoint, counter helper, stylesheet, and starter assets. The browser title was generic. Build output and Node dependencies were not explicitly covered by the root ignore policy. Scratch contained unreferenced experiments and a historical tree, but their purpose was not documented.

## Changes made

- Replaced `README.md` with a release-oriented project overview, locked scope, pipeline, architecture, run instructions, status, and limitations.
- Added `docs/PROJECT_MAP.md`, `docs/FILE_STATUS.md`, `docs/RUNBOOK.md`, and `docs/CHANGE_POLICY.md`.
- Updated `frontend/index.html` title to FOODSHIELD.
- Removed unused Vite starter files: `frontend/src/main.ts`, `counter.ts`, `style.css`, and `assets/hero.png`, `assets/typescript.svg`, `assets/vite.svg`. The active entry remains `main.tsx`; repository search found no remaining references to removed starter material.
- Updated `.gitignore` for pytest cache, Node modules, frontend build output, logs, and temporary files.
- Retained `scratch/test_sens.py`, `scratch/test_script.py`, and `scratch/project_tree.md` as development/review material; no uncertain scratch content was deleted or moved.

## Protected assets

All `data/processed/foodshield/*.csv` SHA-256 hashes were captured before cleanup and compared after cleanup. **0 differences** were found. No raw data, analytical CSV, methodology report, validation report, policy document, figure, API analytical service, or pipeline script was changed.

## Validation

| Check | Result |
|---|---|
| Protected CSV hash comparison | PASS — 0 differences |
| Removed-starter reference search | PASS — no references remain; active `main.tsx` remains |
| README/documentation links | PASS — all four new docs links resolve |
| Frontend build | PASS — `npm.cmd run build` completed |
| Python syntax/import/API validation | NOT RUN — no Python runtime is installed in this environment |

## Not changed

Methodology, analytical CSVs, API analytical behavior, replacement engine, supplier shock, HEEC, resilience profiles, sensitivity methodology, and dashboard analytical behavior are unchanged. The Rank-1-only Replacement Pathway implementation was not reopened or changed.

## Remaining issues

- Live FastAPI/API/browser verification requires a Python-enabled environment.
- Vite reports a future `__dirname` compatibility warning and a bundle-size warning; these were intentionally not addressed.
- Scratch artifacts and generated build output remain intentionally retained/ignored pending future review.

## Final repository status

**READY WITH WARNINGS** — repository organization and documentation are improved, protected assets are unchanged, and the frontend builds. Runtime backend/browser verification remains outstanding because the environment lacks Python.
