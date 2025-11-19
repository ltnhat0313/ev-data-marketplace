from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import routes
from app.api import auth_routes, user_routes  # ✅ thêm 2 dòng này
from app.api import dataset_routes
from app.api import transaction_routes
from app.api import admin_routes
from app.api import provider_routes
from app.core.database import Base, engine
import os

app = FastAPI(title="EV Data Marketplace API")

# ✅ include tất cả các router
app.include_router(routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(dataset_routes.router)
app.include_router(transaction_routes.router)
app.include_router(admin_routes.router)
app.include_router(provider_routes.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & Templates
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Khởi tạo DB & thư mục uploads khi start
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    # Trang chủ hiển thị Dashboard UI
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/ui/upload", response_class=HTMLResponse)
def ui_upload(request: Request):
    return templates.TemplateResponse("provide_upload.html", {"request": request})

@app.get("/ui/search", response_class=HTMLResponse)
def ui_search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/ui/dashboard", response_class=HTMLResponse)
def ui_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/ui/login", response_class=HTMLResponse)
def ui_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/ui/register", response_class=HTMLResponse)
def ui_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/ui/my-datasets", response_class=HTMLResponse)
def ui_my_datasets(request: Request):
    return templates.TemplateResponse("my_datasets.html", {"request": request})

@app.get("/ui/profile", response_class=HTMLResponse)
def ui_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

# ✅ GIỮ PHIÊN BẢN CÓ THAM SỐ ID TỪ MAIN (Đúng logic chi tiết dataset)
@app.get("/ui/dataset/{dataset_id}", response_class=HTMLResponse)
def ui_dataset_detail(request: Request, dataset_id: int):
    return templates.TemplateResponse("dataset_detail.html", {
        "request": request,
        "dataset_id": dataset_id
    })

# ✅ GIỮ CÁC ROUTE MỚI (Từ ui-improvements)
@app.get("/ui/transactions", response_class=HTMLResponse)
def ui_transactions(request: Request):
    return templates.TemplateResponse("transactions.html", {"request": request})

@app.get("/ui/admin", response_class=HTMLResponse)
def ui_admin(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

@app.get("/ui/revenue", response_class=HTMLResponse)
def ui_provider_revenue(request: Request):
    return templates.TemplateResponse("provider_revenue.html", {"request": request})