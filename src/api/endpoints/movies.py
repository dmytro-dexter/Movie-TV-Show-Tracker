from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.crud import crud_movies
from src.schemas import movies
from uuid import UUID
from src.models.users import User
from src.api.endpoints.login import get_current_user

router = APIRouter()


@router.get("", response_model=list[movies.MovieBase])
def get_all_movies(
        args: movies.MoviesGetRequest = Depends(movies.MoviesGetRequest),
        db: Session = Depends(get_db),
) -> list[movies.MovieBase]:
    return crud_movies.get_movies(args, db)


@router.get("/{movie_id}", response_model=movies.MovieBase)
def get_movie_by_id(movie_id: UUID, db: Session = Depends(get_db)) -> movies.MovieBase:
    return crud_movies.get_movie_by_id(movie_id=movie_id, db=db)


@router.post("", response_model=movies.MovieBase,
             description="Rating should be set in 1 to 5 range, otherwise it will be Null")
def create_movie(movie: movies.MovieCreate, db: Session = Depends(get_db)) -> movies.MovieBase:
    return crud_movies.create_movie(db=db, movie=movie)


@router.put("/{movie_id}", response_model=movies.MovieBase,
            description="Rating should be set in 1 to 5 range, otherwise it will be Null")
def movie_update_by_id(movie_id: UUID,
                       movie: movies.MovieUpdate,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> movies.MovieBase:
    movie = crud_movies.update_movie_by_id(movie_id, movie, db, author_id=current_user.id)
    if isinstance(movie, dict):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only author can adjust the movie")
    return movie


@router.delete("/{movie_id}")
def delete_movie_by_id(movie_id: UUID,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)) -> None:
    movie = crud_movies.delete_movie_by_id(movie_id=movie_id, db=db, author_id=current_user.id)
