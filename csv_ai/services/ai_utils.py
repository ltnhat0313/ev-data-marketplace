import pandas as pd
from sqlalchemy.orm import Session
# Dòng này đã được sửa để trỏ đến models.py
from app.models.models import Dataset

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
            "tags": d.tags, # Giả sử bạn có cột 'tags' và 'text_sample'
            "text_sample": d.text_sample
        })
    return pd.DataFrame(data)