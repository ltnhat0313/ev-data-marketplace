from fastapi import FastAPI
from dotenv import load_dotenv
# Import router AI từ thư mục 'api' CÙNG CẤP (csv_ai/api)
try:
    # Nếu chạy từ thư mục csv_ai
    from api.routes import router as ai_router
except ImportError:
    # Nếu chạy từ thư mục gốc (dùng PYTHONPATH)
    # Giả sử 'csv_ai' được coi là một module tên 'app_ai' hoặc tương tự
    # Dựa trên cấu trúc của bạn, có vẻ 'csv_ai' là một gói riêng biệt
    # Hãy thử import tương đối
    from .api.routes import router as ai_router

load_dotenv()

# KHAI BÁO APP CHỈ MỘT LẦN
app = FastAPI(title="EV Data Marketplace - AI Service")

# ✅ Include CHỈ router của service này (AI router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {"message": "Welcome to EV Data Marketplace AI Service 🤖"}

#
# ----- PHẦN BỊ LỖI TRONG FILE GỐC ĐÃ ĐƯỢC XOÁ HOÀN TOÀN -----
# (Toàn bộ phần khai báo app thứ hai và các router auth, user... đã bị xoá)
#