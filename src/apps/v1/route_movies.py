from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.models.movies import Movie
from src.models.reviews import Review
from uuid import UUID

template = Jinja2Templates(directory="src/templates")
router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    context = {"request": request, "movies": movies}
    return template.TemplateResponse("movies/home.html", context=context)


@router.get("/app/movie/{movie_id}")
def movie_detail(request: Request, movie_id: UUID, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    reviews = db.query(Review).filter(Review.movie_id == movie_id).all()
    context = {"request": request, "movie": movie, "reviews": reviews}
    return template.TemplateResponse("movies/detail.html", context=context)
