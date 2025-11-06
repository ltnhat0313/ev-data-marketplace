# tests/test_anonymize.py
import pandas as pd
from app.services.anonymize import anonymize_dataframe, hash_value

def test_hash_value_consistent():
    a = hash_value("user1")
    b = hash_value("user1")
    assert a == b

def test_anonymize_dataframe():
    df = pd.DataFrame({"user_id":[1,2], "email":["a@x.com","b@x.com"], "value":[10,20]})
    out = anonymize_dataframe(df, ["email","user_id"])
    assert out.shape == df.shape
    assert out['value'].tolist() == [10,20]
    # hashed values should not equal original
    assert out['email'][0] != "a@x.com"
