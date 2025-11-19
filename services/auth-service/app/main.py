from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_routes, user_routes
from app.core.database import Base, engine

app = FastAPI(title="EV Auth Service")

@app.on_event("startup")
def on_startup():
    # Tạo bảng database nếu chưa có
    Base.metadata.create_all(bind=engine)

# --- SỬA LỖI ROUTING TẠI ĐÂY ---
# Thêm prefix="/auth" và prefix="/users" để khớp với request từ Traefik.
# Ví dụ: Traefik nhận /api/auth/login -> cắt /api -> gửi /auth/login vào service.
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Auth Service is running 🔒"}