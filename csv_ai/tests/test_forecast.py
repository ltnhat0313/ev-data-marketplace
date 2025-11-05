# tests/test_forecast.py
import pandas as pd
from app.services import ai_forecast

def test_forecast_with_sample_data(tmp_path):
    # 🔹 Tạo dữ liệu giả
    data = pd.DataFrame({
        "date": pd.date_range("2025-10-01", periods=10),
        "downloads": [100, 120, 130, 150, 160, 170, 180, 190, 200, 220]
    })

    # 🔹 Train model Prophet tạm
    ai_forecast.MODEL_DIR = tmp_path
    result = ai_forecast.train_forecast(data, dataset_id="test123")

    assert "model" in result

    # 🔹 Gọi dự báo
    forecast = ai_forecast.forecast_downloads("test123", days=5)

    # 🔹 Kiểm tra định dạng kết quả
    assert len(forecast) == 5
    assert "date" in forecast[0]
    assert "predicted_downloads" in forecast[0]
