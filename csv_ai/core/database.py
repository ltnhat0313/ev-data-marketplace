from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# 1. Đảm bảo import settings từ đúng vị trí
from .config import settings 

# 2. Sử dụng DATABASE_URL từ settings, không hardcode
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 3. Thêm logic kiểm tra nếu là sqlite (giống file app/core/database.py)
engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()