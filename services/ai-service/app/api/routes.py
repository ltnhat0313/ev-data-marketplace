from fastapi import APIRouter, Query
import pandas as pd
from typing import Optional

# Import service từ app.services
from app.services.ai_recommend import recommend_by_text
from app.services.ai_forecast import train_forecast_model, forecast_downloads

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
        print(f"Error in recommend: {e}")
        return {"error": str(e)}

@router.post("/forecast/train")
def train_forecast(dataset_id: int):
    """
    Train mô hình dự báo cho một dataset cụ thể.
    Hiện tại dùng dữ liệu giả lập (mock data).
    """
    try:
        # --- MOCK DATA ---
        data = pd.DataFrame({
            "date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
            "downloads": range(10, 40)
        })
        result = train_forecast_model(data, dataset_id)
        return result
    except Exception as e:
        print(f"Error in train_forecast: {e}")
        return {"error": str(e)}

@router.get("/forecast")
def get_forecast(dataset_id: int, days: int = 7):
    """
    Lấy kết quả dự báo lượt tải cho N ngày tới.
    """
    try:
        result = forecast_downloads(dataset_id, days)
        return {"dataset_id": dataset_id, "forecast": result}
    except FileNotFoundError:
        return {"error": "Mô hình chưa được train. Vui lòng gọi API /ai/forecast/train trước."}
    except Exception as e:
        print(f"Error in get_forecast: {e}")
        return {"error": str(e)}