from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="EV Data Marketplace - Dashboard UI")

# 1. Mount thư mục static (CSS/JS/Images)
# Đường dẫn 'web/static' phải khớp với cấu trúc folder trong container
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# 2. Cấu hình templates (Jinja2)
templates = Jinja2Templates(directory="web/templates")

# --- CÁC ROUTES TRẢ VỀ GIAO DIỆN HTML ---

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Trang chủ mặc định là Dashboard
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/ui/dashboard", response_class=HTMLResponse)
async def ui_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/ui/login", response_class=HTMLResponse)
async def ui_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/ui/register", response_class=HTMLResponse)
async def ui_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/ui/search", response_class=HTMLResponse)
async def ui_search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/ui/upload", response_class=HTMLResponse)
async def ui_upload(request: Request):
    return templates.TemplateResponse("provide_upload.html", {"request": request})

@app.get("/ui/my-datasets", response_class=HTMLResponse)
async def ui_my_datasets(request: Request):
    return templates.TemplateResponse("my_datasets.html", {"request": request})

@app.get("/ui/profile", response_class=HTMLResponse)
async def ui_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/ui/transactions", response_class=HTMLResponse)
async def ui_transactions(request: Request):
    return templates.TemplateResponse("transactions.html", {"request": request})

@app.get("/ui/revenue", response_class=HTMLResponse)
async def ui_revenue(request: Request):
    return templates.TemplateResponse("provider_revenue.html", {"request": request})

@app.get("/ui/admin", response_class=HTMLResponse)
async def ui_admin(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

# Route quan trọng: Xem chi tiết Dataset với ID động
@app.get("/ui/dataset/{dataset_id}", response_class=HTMLResponse)
async def ui_dataset_detail(request: Request, dataset_id: int):
    # Truyền dataset_id vào context để (tùy chọn) render server-side hoặc dùng cho SEO
    return templates.TemplateResponse("dataset_detail.html", {
        "request": request, 
        "dataset_id": dataset_id
    })