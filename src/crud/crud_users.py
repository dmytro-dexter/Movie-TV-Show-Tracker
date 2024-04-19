from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.schemas.users import UserCreate
from src.models.users import User
from src.core.hashing import Hasher
from src.schemas.users import ShowUser
from src.query_builder import get_filtered_query


def create_new_user(user: UserCreate, db: Session):
    user = User(
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_all_users_in_db(db: Session):
    all_users = db.query(User).all()
    return all_users


def get_user_by_id(movie_id: UUID, db: Session) -> ShowUser:
    user_object = get_filtered_query(User, db.query(User), {User.id.key: movie_id}).first()
    if not user_object:
        raise HTTPException(status_code=400, detail=f"Movie ID {movie_id} not found")
    return user_object


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
