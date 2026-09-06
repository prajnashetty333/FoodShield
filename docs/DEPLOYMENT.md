# FOODSHIELD deployment (Render + Vercel)

This document covers hosting only. It does not change analytical methodology.

Imports such as `from backend.api import ...` require the process working directory to be the **repository root**, not `backend/`.

## Render (backend / FastAPI)

Create a **Web Service** from this GitHub repo.

| Setting | Value |
|---|---|
| Root Directory | *leave empty* (repository root) |
| Runtime | Python |
| Python version | `3.13.0` |
| Build Command | `pip install -r backend/requirements.txt` |
| Start Command | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |

Environment variables:

| Name | Required | Notes |
|---|---|---|
| `PYTHON_VERSION` | Recommended | `3.13.0` (avoid 3.14 until pandas/FastAPI wheels are confirmed) |
| `PORT` | Set by Render | Do not hardcode |

A `render.yaml` Blueprint at the repo root encodes the same build/start/Python settings.

Do **not** set Root Directory to `backend`. That breaks `backend.*` imports.

Runtime data files (read-only CSVs under `data/processed/foodshield/`) must be in the Git clone. They are allow-listed in `.gitignore`. Do not upload FAOSTAT raw extracts or the large pipeline-only CSVs (for example replacement candidates). `foodshield_supplier_shock_2010_2023.csv` is about 30 MB; several cached DataFrames may need ~1 GB RAM on Render.

After the service is live, copy the public URL (for example `https://foodshield-api.onrender.com`). The API root `GET /` returns a running message; dashboard routes are under `/api/...`.

## Vercel (frontend / Vite + React)

Create a project with:

| Setting | Value |
|---|---|
| Root Directory | `frontend` |
| Framework | Vite |
| Build Command | `npm run build` (default) |
| Output Directory | `dist` |
| Node | 20.19+ or 22.x |

Environment variables (Production / Preview):

| Name | Required | Example |
|---|---|---|
| `VITE_API_URL` | Yes in production | `https://your-service.onrender.com/api` |

`VITE_API_URL` is inlined at **build** time. Set it before the first production build. If the Render URL changes, update the variable and redeploy.

`frontend/vercel.json` rewrites unknown paths to `index.html` for React Router.

Do not put secrets in `VITE_*` variables; anything with that prefix is visible in the browser bundle.

## Local development

Backend (repo root):

```powershell
py -3.13 -m pip install -r backend/requirements.txt
py -3.13 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Leave `VITE_API_URL` unset locally. Vite proxies `/api` to `http://127.0.0.1:8000`.

## CORS

`backend/main.py` already allows all origins (`allow_origins=["*"]`). A Vercel frontend can call the Render API without a CORS code change. Browsers reject the combination of wildcard origins and credentialed cookies; this dashboard uses Axios without `withCredentials`.
