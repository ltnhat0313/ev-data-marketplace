# tests/test_forecast.py
import pandas as pd
from app.services import ai_forecast
import os # Nên import os để dùng tmp_path

def test_forecast_with_sample_data(tmp_path):
    # 🔹 Tạo dữ liệu giả
    data = pd.DataFrame({
        "date": pd.date_range("2025-10-01", periods=10),
        "downloads": [100, 120, 130, 150, 160, 170, 180, 190, 200, 220]
    })

    # 🔹 Train model Prophet tạm
    # Ghi đè thư mục model để dùng thư mục test tạm thời
    ai_forecast.MODEL_DIR = str(tmp_path)
    
    # ❌ SỬA LỖI TẠI ĐÂY:
    # Tên hàm gốc (bị lỗi): ai_forecast.train_forecast(data, dataset_id="test123")
    # Tên hàm đúng là 'train_forecast_model'
    result = ai_forecast.train_forecast_model(data, dataset_id="test123")

    # Kiểm tra xem file model đã được tạo chưa
    assert "model_path" in result
    assert os.path.exists(result["model_path"])

    # 🔹 Gọi dự báo
    forecast = ai_forecast.forecast_downloads(dataset_id="test123", periods=5)

    # 🔹 Kiểm tra định dạng kết quả
    assert len(forecast) == 5
    
    # ❌ SỬA LỖI TẠI ĐÂY:
    # Tên cột gốc (bị lỗi): 'date' và 'predicted_downloads'
    # Dựa trên file ai_forecast.py, tên cột đúng là 'ds' và 'yhat'
    assert "ds" in forecast[0]
    assert "yhat" in forecast[0]