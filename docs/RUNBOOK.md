# FOODSHIELD Runbook

Python packages are listed in `requirements.txt`; frontend dependencies are in `frontend/package.json`. This workspace currently has no usable Python runtime.

Run FastAPI: `py -3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`.

From `frontend/`, run `npm install`, `npm run dev`, or `npm run build`.

`scripts/validate_9i.py` reconciles baseline/sensitivity/Sankey outputs. `scripts/test_api.py` tests API routes while FastAPI runs. Both require Python.

Pipeline scripts under `src/` read large inputs and write locked outputs. Do **not** run them casually. For final verification, build the frontend, start FastAPI, run API tests, inspect all routes, and compare protected CSV hashes before/after.
