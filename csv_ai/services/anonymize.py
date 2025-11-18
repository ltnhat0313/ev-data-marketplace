import hashlib
import pandas as pd
from typing import List

SALT = "ev_marketplace_secret_salt"  # load from env in real app


def hash_value(val: str, salt: str = SALT) -> str:
    if pd.isna(val):
        return val
    hv = hashlib.sha256(f"{salt}:{val}".encode("utf-8")).hexdigest()
    return hv


def anonymize_dataframe(df: pd.DataFrame, pii_columns: List[str]) -> pd.DataFrame:
    """Replace values in pii_columns with hashed tokens."""
    df = df.copy()
    for col in pii_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(lambda v: hash_value(v))
    return df
