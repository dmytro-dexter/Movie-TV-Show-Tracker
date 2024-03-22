from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.crud import crud_movies
from src.schemas import movies

router = APIRouter()


@router.get("", response_model=list[movies.MovieBase])
def get_all_movies(
        args: movies.MoviesGetRequest = Depends(movies.MoviesGetRequest),
        db: Session = Depends(get_db),
) -> list[movies.MovieBase]:
    return crud_movies.get_movies(args, db)


@router.get("/{movie_id}", response_model=movies.MovieBase)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)) -> movies.MovieBase:
    return crud_movies.get_movie_by_id(movie_id=movie_id, db=db)


@router.post("", response_model=movies.MovieBase,
             description="Rating should be set in 1 to 5 range, otherwise it will be Null")
def create_movie(movie: movies.MovieCreate, db: Session = Depends(get_db)) -> movies.MovieBase:
    return crud_movies.create_movie(db=db, movie=movie)


@router.put("/{movie_id}", response_model=movies.MovieBase,
            description="Rating should be set in 1 to 5 range, otherwise it will be Null")
def movie_update_by_id(movie_id: int,
                       movie: movies.MovieUpdate,
                       db: Session = Depends(get_db)) -> movies.MovieBase:
    return crud_movies.update_movie_by_id(movie_id, movie, db)


@router.delete("/{movie_id}")
def delete_movie_by_id(movie_id: int, db: Session = Depends(get_db)) -> None:
    crud_movies.delete_movie_by_id(movie_id=movie_id, db=db)
