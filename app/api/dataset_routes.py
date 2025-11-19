from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
from app.core.database import SessionLocal
from app.models.models import Dataset, User, Transaction
from app.api.user_routes import get_current_user
import os

router = APIRouter(prefix="/datasets", tags=["Datasets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search")
def search_datasets(
    q: Optional[str] = Query(default=None, description="Từ khóa tiêu đề/mô tả"),
    min_price: Optional[float] = Query(default=None),
    max_price: Optional[float] = Query(default=None),
    owner_id: Optional[int] = Query(default=None),
    start_date: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    sort_by: str = Query(default="created_at", description="created_at|price|title"),
    sort_dir: str = Query(default="desc", description="asc|desc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Dataset)

    if q:
        like = f"%{q}%"
        query = query.filter((Dataset.title.ilike(like)) | (Dataset.description.ilike(like)))

    if min_price is not None:
        query = query.filter(Dataset.price >= min_price)
    if max_price is not None:
        query = query.filter(Dataset.price <= max_price)

    if owner_id is not None:
        query = query.filter(Dataset.owner_id == owner_id)

    def parse_date(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Sai định dạng ngày. Dùng YYYY-MM-DD")

    sd = parse_date(start_date)
    ed = parse_date(end_date)
    if sd is not None:
        query = query.filter(Dataset.created_at >= sd)
    if ed is not None:
        query = query.filter(Dataset.created_at <= ed)

    sort_map = {
        "created_at": Dataset.created_at,
        "price": Dataset.price,
        "title": Dataset.title,
    }
    sort_col = sort_map.get(sort_by, Dataset.created_at)
    if sort_dir.lower() == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": d.id,
                "title": d.title,
                "description": d.description,
                "price": d.price,
                "owner_id": d.owner_id,
                "created_at": d.created_at.isoformat() if d.created_at else None,
            }
            for d in items
        ],
    }


@router.get("/stats/summary")
def datasets_summary(db: Session = Depends(get_db)):
    users_count = db.query(func.count(User.id)).scalar() or 0
    datasets_count = db.query(func.count(Dataset.id)).scalar() or 0
    transactions_count = db.query(func.count(Transaction.id)).scalar() or 0

    latest = (
        db.query(Dataset)
        .order_by(Dataset.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "users": users_count,
        "datasets": datasets_count,
        "transactions": transactions_count,
        "latest": [
            {
                "id": d.id,
                "title": d.title,
                "price": d.price,
                "created_at": d.created_at.isoformat() if d.created_at else None,
            }
            for d in latest
        ],
    }


@router.post("/upload")
def upload_dataset(
    title: str = Form(...),
    description: str = Form("") ,
    price: float = Form(0.0),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ tệp CSV")

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    safe_name = file.filename.replace("..", "_")
    save_path = os.path.join(upload_dir, safe_name)

    with open(save_path, "wb") as f:
        f.write(file.file.read())

    dataset = Dataset(
        title=title,
        description=description,
        price=price,
        file_path=save_path,
        owner_id=current_user.id,
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    return {
        "id": dataset.id,
        "title": dataset.title,
        "price": dataset.price,
        "file_path": dataset.file_path,
        "owner_id": dataset.owner_id,
        "created_at": dataset.created_at.isoformat() if dataset.created_at else None,
    }


@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    d: Dataset | None = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset không tồn tại")
    
    # Get owner info
    owner = db.query(User).filter(User.id == d.owner_id).first()
    
    return {
        "id": d.id,
        "title": d.title,
        "description": d.description,
        "price": d.price,
        "owner_id": d.owner_id,
        "owner_username": owner.username if owner else None,
        "file_path": d.file_path,
        "created_at": d.created_at.isoformat() if d.created_at else None,
    }


@router.get("/mine")
def my_datasets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = (
        db.query(Dataset)
        .filter(Dataset.owner_id == current_user.id)
        .order_by(Dataset.created_at.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "price": d.price,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in items
    ]


@router.put("/{dataset_id}")
def update_dataset(
    dataset_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d: Dataset | None = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset không tồn tại")
    if d.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Không có quyền sửa dataset này")
    if title is not None:
        d.title = title
    if description is not None:
        d.description = description
    if price is not None:
        d.price = price
    db.commit()
    db.refresh(d)
    return {
        "id": d.id,
        "title": d.title,
        "description": d.description,
        "price": d.price,
        "created_at": d.created_at.isoformat() if d.created_at else None,
    }


@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d: Dataset | None = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset không tồn tại")
    if d.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Không có quyền xóa dataset này")
    db.delete(d)
    db.commit()
    return {"ok": True}
@router.get("/{dataset_id}")
def get_dataset_detail(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    d = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset không tồn tại")

    # Đọc 10 dòng đầu của file CSV
    preview_lines = []
    try:
        with open(d.file_path, "r", encoding="utf-8") as f:
            for i in range(10):
                line = f.readline()
                if not line:
                    break
                preview_lines.append(line.strip())
    except:
        preview_lines = ["Không thể đọc file"]

    return {
        "id": d.id,
        "title": d.title,
        "description": d.description,
        "price": d.price,
        "owner_id": d.owner_id,
        "created_at": d.created_at.isoformat() if d.created_at else None,
        "preview": preview_lines
    }


