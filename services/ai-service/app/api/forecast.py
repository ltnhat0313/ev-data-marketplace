# csv_ai/api/forecast.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
# SỬA DÒNG NÀY:
from csv_ai.services.ai_forecast import forecast_downloads # Sửa tên hàm import cho khớp thực tế

router = APIRouter(prefix="/ai", tags=["ai"])

class ForecastRequest(BaseModel):
    dataset_id: str # Lưu ý: service forecast đang dùng int, hãy đồng bộ kiểu dữ liệu
    periods: Optional[int] = 30
    freq: Optional[str] = "D"

@router.post("/forecast")
def get_forecast(req: ForecastRequest):
    # SỬA DÒNG NÀY:
    results = forecast_downloads(int(req.dataset_id), periods=req.periods)
    return {"dataset_id": req.dataset_id, "forecast": results}