from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.models import User

# Lưu ý: URL này chỉ để Swagger UI hiển thị form login, logic check token nằm ở code dưới
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

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
        # 1. Giải mã Token bằng SECRET_KEY chung
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 2. Tìm user trong market_db
    user = db.query(User).filter(User.email == email).first()
    
    # 3. [QUAN TRỌNG] JIT Provisioning: 
    # Nếu Token hợp lệ (đã ký bởi Auth Service) mà User chưa có trong Marketplace
    # -> Tạo ngay một bản ghi User mới để đồng bộ.
    if user is None:
        print(f"⚠️ User {email} chưa tồn tại trong Market DB. Đang tạo mới đồng bộ...")
        # Lấy username tạm từ email (hoặc có thể decode thêm từ token nếu token chứa username)
        username_placeholder = email.split("@")[0]
        
        new_user = User(
            email=email,
            username=username_placeholder,
            role="consumer", # Mặc định là consumer, Admin có thể sửa sau
            hashed_password="managed_by_auth_service" # Marketplace không cần password thật
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    return user