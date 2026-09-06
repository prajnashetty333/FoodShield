import pandas as pd
from functools import lru_cache
import numpy as np
import config as cfg
import os

class DataLoader:
    """
    Centralized data loading service.
    Loads validated FOODSHIELD CSVs and enforces read-only access.
    """
    
    @staticmethod
    def _read_csv_safe(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Validated dataset not found: {file_path}")
        # Replace NaN with None for JSON serialization compatibility later if needed, 
        # but for Pandas, we keep NaN and handle it in the service layer to avoid zero-filling.
        return pd.read_csv(file_path)

    @classmethod
    @lru_cache(maxsize=1)
    def get_resilience_metrics(cls) -> pd.DataFrame:
        df = cls._read_csv_safe(cfg.FILE_RESILIENCE_METRICS)
        # Filter for primary scenario scope
        df = df[
            (df['shock_rank'] == cfg.DEFAULT_SHOCK_RANK) &
            (df['year'].isin(cfg.LOCKED_YEARS)) &
            (df['commodity'].isin(cfg.LOCKED_COMMODITIES)) &
            (df['capacity_status'] == 'capacity_available')
        ]
        return df.copy()

    @classmethod
    @lru_cache(maxsize=1)
    def get_replacement_results(cls) -> pd.DataFrame:
        df = cls._read_csv_safe(cfg.FILE_REPLACEMENT_RESULTS)
        df = df[
            (df['shock_rank'] == cfg.DEFAULT_SHOCK_RANK) &
            (df['year'].isin(cfg.LOCKED_YEARS)) &
            (df['commodity'].isin(cfg.LOCKED_COMMODITIES)) &
            (df['capacity_status'] == 'capacity_available')
        ]
        return df.copy()

    @classmethod
    @lru_cache(maxsize=1)
    def get_supplier_shock(cls) -> pd.DataFrame:
        df = cls._read_csv_safe(cfg.FILE_SUPPLIER_SHOCK)
        df = df[
            (df['year'].isin(cfg.LOCKED_YEARS)) &
            (df['commodity'].isin(cfg.LOCKED_COMMODITIES))
        ]
        # Supplier shock file might not have capacity_status natively, it's just raw shock data.
        return df.copy()

    @classmethod
    @lru_cache(maxsize=1)
    def get_exposure_metrics(cls) -> pd.DataFrame:
        df = cls._read_csv_safe(cfg.FILE_EXPOSURE_METRICS)
        df = df[
            (df['year'].isin(cfg.LOCKED_YEARS)) &
            (df['commodity'].isin(cfg.LOCKED_COMMODITIES))
        ]
        return df.copy()

    @classmethod
    @lru_cache(maxsize=1)
    def get_sensitivity_summary(cls) -> pd.DataFrame:
        df = cls._read_csv_safe(cfg.FILE_SENSITIVITY_SUMMARY)
        return df.copy()

    @classmethod
    @lru_cache(maxsize=1)
    def get_sensitivity_transitions(cls) -> pd.DataFrame:
        df = cls._read_csv_safe(cfg.FILE_SENSITIVITY_TRANSITIONS)
        return df.copy()
        
    @classmethod
    @lru_cache(maxsize=1)
    def get_research_findings(cls) -> pd.DataFrame:
        df = cls._read_csv_safe(cfg.FILE_RESEARCH_FINDINGS)
        return df.copy()

data_loader = DataLoader()
