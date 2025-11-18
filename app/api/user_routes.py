from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.models import User, TwoFactorSecret
from app.schemas.user_schema import UserOut
from app.schemas.user_schema import ChangePasswordInput
from app.core.security import get_password_hash, verify_password
import pyotp
import qrcode
import io
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/change-password")
def change_password(
    body: ChangePasswordInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mật khẩu cũ không đúng")
    current_user.hashed_password = get_password_hash(body.new_password)
    db.add(current_user)
    db.commit()
    return {"ok": True}


@router.get("/me/twofa/status")
def twofa_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(TwoFactorSecret).filter(TwoFactorSecret.user_id == current_user.id).first()
    return {"enabled": bool(rec and rec.enabled)}


@router.post("/me/twofa/setup")
def twofa_setup(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(TwoFactorSecret).filter(TwoFactorSecret.user_id == current_user.id).first()
    if rec and rec.enabled:
        raise HTTPException(status_code=400, detail="2FA đã bật")
    secret = pyotp.random_base32()
    if not rec:
        rec = TwoFactorSecret(user_id=current_user.id, secret=secret, enabled=False)
        db.add(rec)
    else:
        rec.secret = secret
        rec.enabled = False
    db.commit()
    issuer = settings.PROJECT_NAME
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.email, issuer_name=issuer)
    return {"secret": secret, "otpauth_url": uri}


@router.post("/me/twofa/enable")
def twofa_enable(code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(TwoFactorSecret).filter(TwoFactorSecret.user_id == current_user.id).first()
    if not rec:
        raise HTTPException(status_code=400, detail="Chưa setup 2FA")
    totp = pyotp.TOTP(rec.secret)
    if not totp.verify(code, valid_window=1):
        raise HTTPException(status_code=400, detail="Mã 2FA không hợp lệ")
    rec.enabled = True
    db.commit()
    return {"enabled": True}


@router.post("/me/twofa/disable")
def twofa_disable(code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(TwoFactorSecret).filter(TwoFactorSecret.user_id == current_user.id).first()
    if not rec or not rec.enabled:
        raise HTTPException(status_code=400, detail="2FA chưa bật")
    totp = pyotp.TOTP(rec.secret)
    if not totp.verify(code, valid_window=1):
        raise HTTPException(status_code=400, detail="Mã 2FA không hợp lệ")
    rec.enabled = False
    db.commit()
    return {"enabled": False}


@router.get("/me/twofa/qr")
def twofa_qr(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rec = db.query(TwoFactorSecret).filter(TwoFactorSecret.user_id == current_user.id).first()
    if not rec or not rec.secret:
        raise HTTPException(status_code=400, detail="Chưa setup 2FA")
    uri = pyotp.totp.TOTP(rec.secret).provisioning_uri(name=current_user.email, issuer_name=settings.PROJECT_NAME)
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")