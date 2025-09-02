from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, crud, models

router = APIRouter(prefix="/wallets", tags=["Wallets"])

@router.post("/{user_id}/update", response_model=schemas.TransactionOut, summary="Update Wallet (credit/debit)")
def update_wallet(user_id: int, payload: schemas.WalletUpdate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        tx = crud.add_transaction_and_update_balance(
            db, user, payload.amount, payload.description, allow_negative=payload.allow_negative
        )
        return tx
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}/transactions", response_model=List[schemas.TransactionOut], summary="Fetch Transactions for a user")
def fetch_transactions(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.list_transactions(db, user_id)
