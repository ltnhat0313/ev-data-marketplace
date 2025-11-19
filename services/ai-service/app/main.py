from fastapi import FastAPI
import os
from app.core.database import Base, engine
from app.api.routes import router as ai_router
# Import hàm train và hàm load dữ liệu mới sửa
from app.services.ai_recommend import train_tfidf
from app.services.ai_utils import load_metadata_from_csv

app = FastAPI(title="EV Data Marketplace - AI Service")

@app.on_event("startup")
def on_startup():
    # 1. Tạo bảng DB (giữ nguyên để tránh lỗi kết nối)
    Base.metadata.create_all(bind=engine)
    os.makedirs("models", exist_ok=True)
    
    # 2. Tự động Train model từ file CSV khi khởi động
    try:
        print("🤖 Đang train model AI từ datasets.csv...")
        df = load_metadata_from_csv()
        if not df.empty:
            train_tfidf(df)
            print("✅ Train model thành công!")
        else:
            print("⚠️ Không tìm thấy dữ liệu CSV để train.")
    except Exception as e:
        print(f"❌ Lỗi khi train model: {e}")

app.include_router(ai_router)

@app.get("/")
def root():
    return {"message": "Welcome to EV Data Marketplace AI Service 🤖"}