from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import Transaction, Dataset, User
from app.api.user_routes import get_current_user
from typing import Optional

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


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
	# Verify dataset exists
	d = db.query(Dataset).filter(Dataset.id == dataset_id).first()
	if not d:
		raise HTTPException(status_code=404, detail="Dataset không tồn tại")

	# Create a transaction record
	tx = Transaction(user_id=current_user.id, dataset_id=d.id)
	db.add(tx)
	db.commit()
	db.refresh(tx)

	# In a real system, this would return a signed URL or gated download token
	return {
		"ok": True,
		"transaction_id": tx.id,
		"dataset_id": d.id,
		"message": "Giao dịch đã tạo thành công",
	}
