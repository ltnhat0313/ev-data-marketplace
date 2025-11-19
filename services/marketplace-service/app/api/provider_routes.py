from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import SessionLocal
from app.models.models import User, Dataset, Transaction
# --- SỬA DÒNG DƯỚI ĐÂY ---
from app.api.deps import get_db, get_current_user 

router = APIRouter(prefix="/provider", tags=["Provider"])

# (Không cần định nghĩa lại get_db vì đã import từ deps)

@router.get("/revenue")
def get_revenue_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get all datasets owned by current user
    datasets = db.query(Dataset).filter(Dataset.owner_id == current_user.id).all()
    dataset_ids = [d.id for d in datasets]
    
    if not dataset_ids:
        return {
            "total_revenue": 0,
            "total_sales": 0,
            "datasets_count": 0,
            "datasets": []
        }
    
    # Get transactions for these datasets
    transactions = db.query(Transaction).filter(Transaction.dataset_id.in_(dataset_ids)).all()
    
    # Calculate revenue per dataset
    dataset_stats = []
    for dataset in datasets:
        dataset_txs = [tx for tx in transactions if tx.dataset_id == dataset.id]
        revenue = dataset.price * len(dataset_txs)
        dataset_stats.append({
            "id": dataset.id,
            "title": dataset.title,
            "price": dataset.price,
            "sales_count": len(dataset_txs),
            "revenue": revenue,
            "created_at": dataset.created_at.isoformat() if dataset.created_at else None,
        })
    
    total_revenue = sum(d["revenue"] for d in dataset_stats)
    total_sales = len(transactions)
    
    return {
        "total_revenue": total_revenue,
        "total_sales": total_sales,
        "datasets_count": len(datasets),
        "datasets": dataset_stats,
    }