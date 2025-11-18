# app/api/ai_router.py
from fastapi import APIRouter, Query
from app.services.ai_recommend import recommend_by_text

router = APIRouter(prefix="/ai", tags=["AI"])

@router.get("/recommend")
def recommend_datasets(
    query: str = Query(..., description="Nhập tiêu đề hoặc mô tả dataset để tìm dataset tương tự"),
    top_k: int = Query(5, description="Số lượng dataset gợi ý muốn lấy (mặc định 5)")
):
    try:
        results = recommend_by_text(query, top_k=top_k)
        if not results:
            return {"query": query, "message": "Không tìm thấy dataset tương tự nào."}
        return {"query": query, "recommendations": results}
    except Exception as e:
        return {"error": str(e)}
from app.services.ai_forecast import train_forecast_model, forecast_downloads
import pandas as pd

@router.post("/ai/forecast/train", tags=["AI"])
def train_forecast(dataset_id: int):
    """
    Train mô hình Prophet dựa trên dữ liệu mock hoặc thực tế
    """
    # Giả sử bạn đang dùng dữ liệu mẫu (có thể sau này lấy từ DB)
    df = pd.read_csv("data/downloads_sample.csv")
    result = train_forecast_model(df, dataset_id)
    return result


@router.get("/ai/forecast", tags=["AI"])
def get_forecast(dataset_id: int, days: int = 7):
    """
    Lấy dự báo lượt tải cho N ngày tới
    """
    try:
        result = forecast_downloads(dataset_id, days)
        return {"dataset_id": dataset_id, "forecast": result}
    except Exception as e:
        return {"error": str(e)}
