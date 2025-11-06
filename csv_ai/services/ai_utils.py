import pandas as pd
from sqlalchemy.orm import Session
from app.models.dataset import Dataset

def load_metadata_from_db(db: Session):
    """
    Đọc metadata từ bảng datasets để train TF-IDF
    """
    datasets = db.query(Dataset).all()
    data = []
    for d in datasets:
        data.append({
            "id": str(d.id),
            "title": d.title,
            "description": d.description,
            "tags": d.tags,
            "text_sample": d.text_sample
        })
    return pd.DataFrame(data)
