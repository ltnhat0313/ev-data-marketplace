# tests/test_tfidf.py
import pandas as pd
from app.services.ai_recommend import train_tfidf, recommend_by_text, load_model
import os

def test_tfidf_training_and_recommend(tmp_path):
    # small dataset
    df = pd.DataFrame([
        {"id":"d1","title":"electric vehicle charging","description":"charging station data","tags":"ev charging","text_sample":""},
        {"id":"d2","title":"battery health","description":"battery degradation patterns","tags":"battery","text_sample":""},
    ])
    # place models into tmp to avoid clutter
    os.environ['MODEL_DIR'] = str(tmp_path)
    out = train_tfidf(df)
    vec, mat, ids = load_model()
    res = recommend_by_text("battery", top_k=1)
    assert len(res) >= 1
    assert res[0]['dataset_id'] in ids
