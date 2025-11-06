<<<<<<< HEAD
from fastapi import FastAPI
from app.api import routes
from app.api import auth_routes, user_routes  # ✅ thêm 2 dòng này
=======
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import routes
from app.api import auth_routes, user_routes  # ✅ thêm 2 dòng này
from app.api import dataset_routes
from app.api import transaction_routes
from app.core.database import Base, engine
import os
>>>>>>> nam

app = FastAPI(title="EV Data Marketplace API")

# ✅ include tất cả các router
app.include_router(routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
<<<<<<< HEAD

@app.get("/")
def root():
    return {"message": "Welcome to EV Data Marketplace API 🚗"}
=======
app.include_router(dataset_routes.router)
app.include_router(transaction_routes.router)

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
>>>>>>> nam
