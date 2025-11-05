# app/services/ai_recommend.py
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import List, Dict

MODEL_DIR = os.getenv("MODEL_DIR", "models")

def build_corpus_from_metadata(datasets: pd.DataFrame) -> List[str]:
    # datasets: DataFrame with columns ['id','title','description','tags','text_sample']
    def row_text(r):
        parts = []
        for c in ['title','description','tags','text_sample']:
            if c in r and pd.notna(r[c]):
                parts.append(str(r[c]))
        return " ".join(parts)
    return datasets.apply(row_text, axis=1).tolist()

def train_tfidf(datasets: pd.DataFrame, model_name: str = "tfidf"):
    corpus = build_corpus_from_metadata(datasets)
    vectorizer = TfidfVectorizer(max_df=0.9, min_df=1, ngram_range=(1,2))
    tfidf_matrix = vectorizer.fit_transform(corpus)
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, f"{model_name}_vectorizer.joblib"))
    joblib.dump(tfidf_matrix, os.path.join(MODEL_DIR, f"{model_name}_matrix.joblib"))
    # Save id order
    joblib.dump(list(datasets['id']), os.path.join(MODEL_DIR, f"{model_name}_ids.joblib"))
    # === Save mapping dataset_id -> index ===
    id_to_index = {row_id: i for i, row_id in enumerate(list(datasets["id"]))}
    joblib.dump(id_to_index, os.path.join(MODEL_DIR, f"{model_name}_id_map.joblib"))

    return {
        "vectorizer": os.path.join(MODEL_DIR, f"{model_name}_vectorizer.joblib"),
        "matrix": os.path.join(MODEL_DIR, f"{model_name}_matrix.joblib"),
        "ids": os.path.join(MODEL_DIR, f"{model_name}_ids.joblib")
    }

def load_model(model_name: str = "tfidf"):
    vec = joblib.load(os.path.join(MODEL_DIR, f"{model_name}_vectorizer.joblib"))
    mat = joblib.load(os.path.join(MODEL_DIR, f"{model_name}_matrix.joblib"))
    ids = joblib.load(os.path.join(MODEL_DIR, f"{model_name}_ids.joblib"))
    return vec, mat, ids

def recommend_by_text(query: str, top_k: int = 5, model_name: str = "tfidf"):
    vec, mat, ids = load_model(model_name)
    q_vec = vec.transform([query])
    # cosine similarity via linear_kernel (fast for sparse)
    cos_sim = linear_kernel(q_vec, mat).flatten()
    top_idx = np.argsort(cos_sim)[::-1][:top_k]
    return [{"dataset_id": ids[i], "score": float(cos_sim[i])} for i in top_idx if cos_sim[i] > 0]
