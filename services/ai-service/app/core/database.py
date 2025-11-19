from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# SỬA: Dùng đường dẫn tuyệt đối
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine_kwargs = {}
# Chỉ thêm check_same_thread nếu fallback về sqlite
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()