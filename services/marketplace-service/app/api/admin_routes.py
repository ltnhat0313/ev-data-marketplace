from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import User, Dataset, Transaction
# SỬA DÒNG NÀY: Import từ deps
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Chỉ admin mới có quyền truy cập")
    return current_user

@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    total = db.query(func.count(User.id)).scalar() or 0
    users = db.query(User).offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role,
            }
            for u in users
        ],
    }

@router.get("/datasets")
def list_all_datasets(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    total = db.query(func.count(Dataset.id)).scalar() or 0
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for d in datasets:
        owner = db.query(User).filter(User.id == d.owner_id).first()
        result.append({
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "price": d.price,
            "owner_id": d.owner_id,
            "owner_username": owner.username if owner else None,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        })
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": result,
    }

@router.get("/transactions")
def list_all_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    total = db.query(func.count(Transaction.id)).scalar() or 0
    transactions = db.query(Transaction).order_by(Transaction.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for tx in transactions:
        user = db.query(User).filter(User.id == tx.user_id).first()
        dataset = db.query(Dataset).filter(Dataset.id == tx.dataset_id).first()
        result.append({
            "id": tx.id,
            "user_id": tx.user_id,
            "user_email": user.email if user else None,
            "dataset_id": tx.dataset_id,
            "dataset_title": dataset.title if dataset else None,
            "timestamp": tx.timestamp.isoformat() if tx.timestamp else None,
        })
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": result,
    }

@router.get("/stats")
def admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    users_count = db.query(func.count(User.id)).scalar() or 0
    datasets_count = db.query(func.count(Dataset.id)).scalar() or 0
    transactions_count = db.query(func.count(Transaction.id)).scalar() or 0
    
    consumers = db.query(func.count(User.id)).filter(User.role == "consumer").scalar() or 0
    providers = db.query(func.count(User.id)).filter(User.role == "provider").scalar() or 0
    admins = db.query(func.count(User.id)).filter(User.role == "admin").scalar() or 0
    
    total_revenue = db.query(func.sum(Dataset.price)).join(Transaction, Dataset.id == Transaction.dataset_id).scalar() or 0
    
    return {
        "users": {
            "total": users_count,
            "consumers": consumers,
            "providers": providers,
            "admins": admins,
        },
        "datasets": datasets_count,
        "transactions": transactions_count,
        "total_revenue": float(total_revenue) if total_revenue else 0,
    }

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    new_role: str = Query(..., description="consumer|provider|admin"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if new_role not in ["consumer", "provider", "admin"]:
        raise HTTPException(status_code=400, detail="Role không hợp lệ")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }

@router.delete("/datasets/{dataset_id}")
def admin_delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset không tồn tại")
    
    db.delete(dataset)
    db.commit()
    return {"ok": True, "message": "Dataset đã được xóa"}