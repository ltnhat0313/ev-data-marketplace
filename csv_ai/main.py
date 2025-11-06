from fastapi import FastAPI
from app.api import routes
from app.api import auth_routes, user_routes  
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(title="EV Data Marketplace API")

# ✅ include tất cả các router
app.include_router(routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to EV Data Marketplace API 🚗"}

from fastapi import FastAPI
from app.api import ai_router

app = FastAPI()

app.include_router(ai_router.router)
