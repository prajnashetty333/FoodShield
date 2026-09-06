import pandas as pd
from functools import lru_cache
import config as cfg

@lru_cache(maxsize=1)
def _load_mappings():
    df = pd.read_csv(
        cfg.FILE_SUPPLIER_SHOCK,
        usecols=['importer_country_code', 'importer_country_name']
    ).drop_duplicates()
    code_to_name = dict(zip(df['importer_country_code'].astype(str), df['importer_country_name']))
    name_to_code = dict(zip(df['importer_country_name'], df['importer_country_code'].astype(str)))
    return code_to_name, name_to_code

def get_country_name(code_or_name: str) -> str:
    code_to_name, _ = _load_mappings()
    return code_to_name.get(str(code_or_name), str(code_or_name))

def get_country_code(code_or_name: str) -> str:
    code_to_name, name_to_code = _load_mappings()
    s = str(code_or_name)
    if s in name_to_code:
        return name_to_code[s]
    if s in code_to_name:
        return s
    return s

class DynamicCountryMapping(dict):
    def get(self, key, default=None):
        code_to_name, _ = _load_mappings()
        return code_to_name.get(str(key), default)

    def items(self):
        code_to_name, _ = _load_mappings()
        return code_to_name.items()

    def __getitem__(self, key):
        code_to_name, _ = _load_mappings()
        return code_to_name[str(key)]

    def __contains__(self, key):
        code_to_name, _ = _load_mappings()
        return str(key) in code_to_name

class DynamicReverseMapping(dict):
    def get(self, key, default=None):
        _, name_to_code = _load_mappings()
        return name_to_code.get(str(key), default)

    def items(self):
        _, name_to_code = _load_mappings()
        return name_to_code.items()

    def __getitem__(self, key):
        _, name_to_code = _load_mappings()
        return name_to_code[str(key)]

    def __contains__(self, key):
        _, name_to_code = _load_mappings()
        return str(key) in name_to_code

COUNTRY_MAPPING = DynamicCountryMapping()
REVERSE_COUNTRY_MAPPING = DynamicReverseMapping()
