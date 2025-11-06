<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
=======
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
>>>>>>> nam
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="consumer")

    datasets = relationship("Dataset", back_populates="owner")

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="datasets")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
<<<<<<< HEAD
=======


class TwoFactorSecret(Base):
    __tablename__ = "two_factor_secrets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    secret = Column(String)
    enabled = Column(Boolean, default=False)
>>>>>>> nam
