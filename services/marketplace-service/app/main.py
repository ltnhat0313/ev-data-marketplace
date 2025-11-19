from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Chỉ import các module nghiệp vụ của Marketplace
from app.api import dataset_routes, transaction_routes, admin_routes, provider_routes, routes
from app.core.database import Base, engine
import os

app = FastAPI(title="EV Marketplace Service")

# Khởi tạo DB & folder upload
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    os.makedirs("uploads", exist_ok=True)

# Include router (Đã xóa auth_routes và user_routes)
app.include_router(routes.router)
app.include_router(dataset_routes.router)
app.include_router(transaction_routes.router)
app.include_router(admin_routes.router)
app.include_router(provider_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Marketplace Service is running 🚀"}