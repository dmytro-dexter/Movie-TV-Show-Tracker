from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from src.api.deps import get_db
from src.core.hashing import Hasher
from src.crud.crud_users import get_user_by_email
from src.core.security import create_access_token
from src.settings import ALGORITHM, SECRET_KEY

router = APIRouter()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email=email, db=db)

    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(detail="Incorrect email or password", status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials, Please login again",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise credentials_exception
    return user
