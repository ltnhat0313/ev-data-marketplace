import pandas as pd
from typing import Tuple, List
from .anonymize import anonymize_dataframe

def preview_csv(path: str, n: int = 5) -> pd.DataFrame:
    return pd.read_csv(path, nrows=n)

def validate_csv_columns(path: str, required: List[str]) -> Tuple[bool, List[str]]:
    df = pd.read_csv(path, nrows=0)
    missing = [c for c in required if c not in df.columns]
    return (len(missing) == 0, missing)

def sanitize_and_save(csv_path: str):
    df = pd.read_csv(csv_path)
    df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', c.lower()) for c in df.columns]
    df.fillna("", inplace=True)
    df.to_csv(csv_path, index=False)
    return df

def extract_text_sample(df: pd.DataFrame, max_len=1000):
    text = " ".join(df.astype(str).values.flatten())
    return text[:max_len]
