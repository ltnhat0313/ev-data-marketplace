import pandas as pd
from app.services import ai_recommend

def test_tfidf_train_and_recommend(tmp_path):
    # 🔹 Tạo dữ liệu giả
    data = pd.DataFrame([
        {"id": 1, "title": "Battery performance dataset", "description": "EV battery performance and efficiency"},
        {"id": 2, "title": "Charging habits dataset", "description": "EV charging patterns and frequency"},
        {"id": 3, "title": "Vehicle telemetry dataset", "description": "Speed and torque sensor data"}
    ])

    # 🔹 Train model TF-IDF tạm trong thư mục test
    ai_recommend.MODEL_DIR = tmp_path
    ai_recommend.train_tfidf(data, model_name="test_model")

    # 🔹 Thực hiện gợi ý
    results = ai_recommend.recommend_by_text("battery", top_k=2, model_name="test_model")

    # 🔹 Kiểm tra kết quả
    assert len(results) > 0
    assert isinstance(results[0]["dataset_id"], int)
    assert results[0]["score"] > 0
