# app/api/forecast.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.ai_forecast import forecast

router = APIRouter(prefix="/ai", tags=["ai"])

class ForecastRequest(BaseModel):
    dataset_id: str
    periods: Optional[int] = 30
    freq: Optional[str] = "D"

@router.post("/forecast")
def get_forecast(req: ForecastRequest):
    results = forecast(req.dataset_id, periods=req.periods, freq=req.freq)
    return {"dataset_id": req.dataset_id, "forecast": results}
