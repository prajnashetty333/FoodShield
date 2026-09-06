from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import overview, countries, commodities, shocks, replacement, sensitivity, policy, methodology

app = FastAPI(title="FOODSHIELD Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In a real app, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(overview.router, prefix="/api/overview", tags=["Overview"])
app.include_router(countries.router, prefix="/api/countries", tags=["Countries"])
app.include_router(commodities.router, prefix="/api/commodities", tags=["Commodities"])
app.include_router(shocks.router, prefix="/api/shocks", tags=["Shocks"])
app.include_router(replacement.router, prefix="/api/replacement", tags=["Replacement"])
app.include_router(sensitivity.router, prefix="/api/sensitivity", tags=["Sensitivity"])
app.include_router(policy.router, prefix="/api/policy", tags=["Policy"])
app.include_router(methodology.router, prefix="/api/methodology", tags=["Methodology"])

@app.get("/")
def read_root():
    return {"message": "FOODSHIELD API is running"}
