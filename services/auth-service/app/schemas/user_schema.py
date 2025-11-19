from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Lớp cơ sở, dùng chung
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Dùng khi tạo user mới (Đăng ký)
class UserCreate(UserBase):
    password: str

# Dùng khi trả về thông tin user (API /me, /register)
class UserOut(UserBase):
    id: int
    role: str

    # ✅ ĐÃ SỬA TẠI ĐÂY:
    # 1. Đổi 'class Config' thành 'model_config = ConfigDict(...)'
    # 2. Đổi 'orm_mode = True' thành 'from_attributes = True'
    model_config = ConfigDict(from_attributes=True)

# Dùng khi trả về token (Đăng nhập)
class Token(BaseModel):
    access_token: str
    token_type: str

# Dùng cho form Đăng nhập (có hỗ trợ 2FA)
class LoginInput(BaseModel):
    email: EmailStr
    password: str
    code: Optional[str] = None

# Dùng cho form Đổi mật khẩu
class ChangePasswordInput(BaseModel):
    old_password: str
    new_password: str