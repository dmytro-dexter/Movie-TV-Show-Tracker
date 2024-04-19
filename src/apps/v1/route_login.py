import json

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.schemas.users import UserCreate
from src.crud.crud_users import create_new_user
from pydantic.error_wrappers import ValidationError

templates = Jinja2Templates(directory="src/templates")
router = APIRouter()


@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
def register(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)):
    errors = []
    try:
        user = UserCreate(email=email, password=password)
        create_new_user(user=user, db=db)
        return responses.RedirectResponse("/?alert=Successfully%20Registered", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        error_list = json.loads(e.json())
        for item in error_list:
            errors.append(item.get("loc")[0]+": "+item.get("msg"))
        return templates.TemplateResponse("auth/register.html", {"request": request, "errors": errors})
