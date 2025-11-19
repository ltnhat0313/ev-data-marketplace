import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Cấu hình Database (Mặc định dùng MySQL trong Docker)
    DATABASE_URL: str = "mysql+pymysql://root:161105@mysqldb:3306/market_db"
    
    # Đường dẫn lưu model và upload
    MODEL_DIR: str = "/app/models"
    UPLOAD_DIR: str = "/app/uploads"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()