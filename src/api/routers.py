from fastapi import FastAPI, APIRouter

from src.api.endpoints import movies, reviews, users, login

api_router = APIRouter()
api_router.include_router(movies.router, prefix="/movies", tags=["Movies"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(login.router, prefix="", tags=["Login"])


