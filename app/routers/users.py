from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[schemas.UserOut], summary="List Users")
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@router.post("", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED, summary="Create User (helper)")
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    # prevent duplicates
    if crud.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    if crud.get_user_by_phone(db, data.phone):
        raise HTTPException(status_code=400, detail="Phone already exists")
    return crud.create_user(db, data)
