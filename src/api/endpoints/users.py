from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.schemas.users import UserCreate, ShowUser

from src.api.deps import get_db
from src.crud.crud_users import create_new_user, read_all_users_in_db

router = APIRouter()


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/")
def read_users(db: Session = Depends(get_db)):
    return read_all_users_in_db(db=db)
