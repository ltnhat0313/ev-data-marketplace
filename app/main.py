from fastapi import FastAPI
from app.api import routes
from app.api import auth_routes, user_routes  # ✅ thêm 2 dòng này

app = FastAPI(title="EV Data Marketplace API")

# ✅ include tất cả các router
app.include_router(routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to EV Data Marketplace API 🚗"}
