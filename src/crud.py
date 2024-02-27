from typing import List
from fastapi import HTTPException

from sqlalchemy.orm import Session
import models
import schemas


def find_movie_object_by_id(movie_id: int, db: Session):
    db_object = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    return db_object


def find_movie_object_by_title(title: str, db: Session):
    db_object = db.query(models.Movie).filter(models.Movie.title == title.lower()).first()
    return db_object


def get_movie_by_id(movie_id: int, db: Session):
    db_movie = find_movie_object_by_id(movie_id=movie_id, db=db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie ID {movie_id} not found")
    return db_movie


def get_movie_by_title(title: str, db: Session):
    db_movie = find_movie_object_by_title(title=title, db=db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie with title - {title} not found")
    return db_movie


def get_movies(db: Session) -> List[schemas.MovieBase]:
    movies = db.query(models.Movie).all()
    return [schemas.MovieBase(**item.__dict__) for item in movies]


def create_movie(movie: schemas.MovieCreate, db: Session):
    db_object = find_movie_object_by_title(title=movie.title, db=db)
    if db_object:
        raise HTTPException(status_code=400, detail=f"Movie with title - {movie.title} already created")
    db_movie = models.Movie(
        title=movie.title.lower(),
        description=movie.description,
        watched=movie.watched,
        rating=movie.rating if 1 <= movie.rating <= 5 else None,
        reviews=movie.reviews,
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie_by_title(movie_title: str, movie: schemas.MovieUpdate, db: Session):
    db_movie = find_movie_object_by_title(title=movie_title, db=db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie with title - {movie_title} not found")
    for key, value in schemas.MovieUpdate(**movie.__dict__):
        setattr(db_movie, key, value)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie_by_id(movie_id: int, movie: schemas.MovieUpdate, db: Session):
    db_movie = find_movie_object_by_id(movie_id=movie_id, db=db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie with ID {movie_id} not found")
    for key, value in schemas.MovieUpdate(**movie.__dict__):
        setattr(db_movie, key, value)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie_by_id(movie_id: int, db: Session):
    db_movie = find_movie_object_by_id(movie_id=movie_id, db=db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie ID {movie_id} not found")
    db.delete(db_movie)
    db.commit()


def delete_movie_by_title(title: str, db: Session):
    db_movie = find_movie_object_by_title(title=title, db=db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie with title - {title} not found")
    db.delete(db_movie)
    db.commit()
