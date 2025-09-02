from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., examples=["Alice"])
    email: EmailStr = Field(..., examples=["alice@example.com"])
    phone: str = Field(..., examples=["+91-7000000000"])

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    balance: float

    class Config:
        from_attributes = True

class WalletUpdate(BaseModel):
    amount: float = Field(..., description="Positive for credit, negative for debit")
    description: Optional[str] = Field(default=None, examples=["Initial top-up"])
    allow_negative: bool = Field(default=False, description="Allow balance to go below zero")

class TransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
