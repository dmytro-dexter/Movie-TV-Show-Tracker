from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import crud
import schemas

from deps import get_db

router = APIRouter()


@router.post("/movies/", response_model=schemas.MovieBase,
             description="Rating should be set in 1 to 5 range, otherwise it will be Null")
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)) -> schemas.MovieBase:
    return crud.create_movie(db=db, movie=movie)


@router.get("/movies", response_model=List[schemas.MovieBase])
def get_all_movies(db: Session = Depends(get_db)) -> List[schemas.MovieBase]:
    return crud.get_movies(db)


@router.get("/movies/{movie_id}", response_model=schemas.MovieBase)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)) -> schemas.MovieBase:
    return crud.get_movie_by_id(movie_id=movie_id, db=db)


@router.get("/movies_title/{movie_title}", response_model=schemas.MovieBase)
def get_movie_by_title(movie_title: str, db: Session = Depends(get_db)) -> schemas.MovieBase:
    return schemas.MovieBase(**crud.get_movie_by_title(movie_title, db).__dict__)


@router.put("/movie_update/{movie_title}", response_model=schemas.MovieBase,
            description="Rating should be set in 1 to 5 range, otherwise it will be Null")
def movie_update_by_title(
        movie_title: str,
        movie: schemas.MovieUpdate,
        db: Session = Depends(get_db)) -> schemas.MovieBase:
    return crud.update_movie_by_title(movie_title=movie_title, movie=movie, db=db)


@router.put("/movie_update_by_id/{movie_id}", response_model=schemas.MovieBase,
            description="Rating should be set in 1 to 5 range, otherwise it will be Null")
def movie_update_by_id(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db)) -> schemas.MovieBase:
    return crud.update_movie_by_id(movie_id, movie, db)


@router.delete("/movie_delete/{movie_id}")
def delete_movie_by_id(movie_id: int, db: Session = Depends(get_db)) -> None:
    crud.delete_movie_by_id(movie_id=movie_id, db=db)


@router.delete("/movie_delete_by_title/{movie_title}")
def delete_movie_by_title(title: str, db: Session = Depends(get_db)) -> None:
    crud.delete_movie_by_title(title, db)
