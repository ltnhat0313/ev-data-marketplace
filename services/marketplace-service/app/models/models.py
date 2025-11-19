from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# Định nghĩa lại User y hệt Auth Service để SQLAlchemy hiểu mapping
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(50), default="consumer")

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    price = Column(Float)
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    # Dùng ForeignKey trỏ về users.id vì giờ chúng ta chung DB
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship (tùy chọn, giúp query dễ hơn)
    owner = relationship("User")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)