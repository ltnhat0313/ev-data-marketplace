from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import SessionLocal
from app.models.models import User
from app.schemas.user_schema import UserCreate, Token, UserOut, LoginInput, ChangePasswordInput
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.models.models import TwoFactorSecret
import pyotp

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login_user(form_data: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    # Nếu user bật 2FA, yêu cầu mã TOTP hợp lệ
    tfa = db.query(TwoFactorSecret).filter(TwoFactorSecret.user_id == user.id, TwoFactorSecret.enabled == True).first()
    if tfa:
        if not form_data.code:
            raise HTTPException(status_code=401, detail="2FA code required")
        totp = pyotp.TOTP(tfa.secret)
        if not totp.verify(form_data.code, valid_window=1):
            raise HTTPException(status_code=401, detail="Invalid 2FA code")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/change-password")
def change_password(
    body: ChangePasswordInput,
    db: Session = Depends(get_db),
):
    # Yêu cầu xác thực: tạm dùng email+password cũ hoặc nên dùng current_user (OAuth2). Để đơn giản, dùng email trong token là an toàn hơn.
    raise HTTPException(status_code=400, detail="Use /users/me/change-password in user_routes instead")