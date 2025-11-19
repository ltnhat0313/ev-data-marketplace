from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models.models import Transaction, Dataset, User
from app.api.deps import get_db, get_current_user
import os

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/mine")
def my_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .all()
    )
    
    result = []
    for tx in transactions:
        dataset = db.query(Dataset).filter(Dataset.id == tx.dataset_id).first()
        result.append({
            "id": tx.id,
            "dataset_id": tx.dataset_id,
            "dataset_title": dataset.title if dataset else "N/A",
            "created_at": tx.created_at.isoformat() if tx.created_at else None,
        })
    
    return result

@router.post("/purchase")
def create_purchase(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dataset không tồn tại")

    # Kiểm tra nếu đã mua rồi thì không cần tạo giao dịch mới (Tùy chọn)
    existing_tx = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.dataset_id == d.id
    ).first()
    
    if existing_tx:
        return {
            "ok": True,
            "transaction_id": existing_tx.id,
            "dataset_id": d.id,
            "message": "Bạn đã sở hữu dataset này",
        }

    tx = Transaction(user_id=current_user.id, dataset_id=d.id)
    db.add(tx)
    db.commit()
    db.refresh(tx)

    return {
        "ok": True,
        "transaction_id": tx.id,
        "dataset_id": d.id,
        "message": "Giao dịch đã tạo thành công",
    }

@router.get("/{dataset_id}/download")
def download_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cho phép người dùng tải xuống file dữ liệu sau khi đã mua hoặc là chủ sở hữu.
    """
    d = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not d:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset không tồn tại")

    # 1. Kiểm tra quyền sở hữu (Chủ sở hữu luôn có quyền tải)
    is_owner = d.owner_id == current_user.id

    # 2. Kiểm tra lịch sử mua hàng (Người mua có quyền tải)
    is_purchased = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.dataset_id == dataset_id
    ).first()

    if not is_owner and not is_purchased:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền tải xuống. Vui lòng mua dataset này.")

    file_path = d.file_path
    
    # Kiểm tra tính tồn tại của file trên hệ thống
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File dữ liệu không tồn tại trên server.")

    # Trả về file dưới dạng FileResponse
    file_name = os.path.basename(file_path)
    
    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="text/csv"
    )