import os
import joblib
import pandas as pd
from prophet import Prophet
from datetime import datetime

MODEL_DIR = os.getenv("MODEL_DIR", "models")

def train_forecast_model(df: pd.DataFrame, dataset_id: int):
    """
    Train mô hình Prophet dựa trên dữ liệu lượt tải theo thời gian.
    df phải có 2 cột: 'date' (YYYY-MM-DD) và 'downloads'
    """
    model = Prophet()
    model.fit(df.rename(columns={"date": "ds", "downloads": "y"}))
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, f"forecast_{dataset_id}.joblib")
    joblib.dump(model, path)
    return {"message": f"Model for dataset {dataset_id} trained", "model_path": path}

def forecast_downloads(dataset_id: int, periods: int = 7):
    """
    Dự báo lượt tải tương lai (7 ngày mặc định)
    """
    path = os.path.join(MODEL_DIR, f"forecast_{dataset_id}.joblib")
    if not os.path.exists(path):
        raise FileNotFoundError("Model chưa được train. Hãy train trước.")

    model = joblib.load(path)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)
    return result.to_dict(orient="records")
