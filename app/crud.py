from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from . import models, schemas

def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(name=data.name, email=data.email, phone=data.phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session) -> List[models.User]:
    return db.execute(select(models.User)).scalars().all()

def get_user(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.execute(select(models.User).where(models.User.email == email)).scalars().first()

def get_user_by_phone(db: Session, phone: str) -> models.User | None:
    return db.execute(select(models.User).where(models.User.phone == phone)).scalars().first()

def add_transaction_and_update_balance(db: Session, user: models.User, amount: float, description: str | None, allow_negative: bool = False) -> models.Transaction:
    new_balance = (user.balance or 0.0) + amount
    if not allow_negative and new_balance < 0:
        raise ValueError("Insufficient balance and allow_negative=False")
    user.balance = new_balance
    tx = models.Transaction(user_id=user.id, amount=amount, description=description)
    db.add(tx)
    db.add(user)
    db.commit()
    db.refresh(tx)
    return tx

def list_transactions(db: Session, user_id: int) -> List[models.Transaction]:
    return db.execute(select(models.Transaction).where(models.Transaction.user_id == user_id).order_by(models.Transaction.created_at.desc())).scalars().all()
