from fastapi import FastAPI, APIRouter

from src.api.endpoints import movies, reviews


def register_api(app: FastAPI):
    api_router = APIRouter()
    api_router.include_router(movies.router, prefix="/movies", tags=["Movies"])
    api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])

    app.include_router(api_router)
