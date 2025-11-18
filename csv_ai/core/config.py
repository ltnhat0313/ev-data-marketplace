import os
from dotenv import load_dotenv

load_dotenv()  

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "../uploads"))
MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(BASE_DIR, "../models"))

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
