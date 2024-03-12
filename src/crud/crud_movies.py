from typing import Any

from fastapi import HTTPException, Query
from sqlalchemy.orm import Session

from src.models.models_movies import Movie, Review
from src.schemas import movies as schemas


def get_movie_by_id(movie_id: int, db: Session) -> Movie:
    db_movie = get_filtered_query(Movie, db.query(Movie), {Movie.id.key: movie_id}).first()
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie ID {movie_id} not found")
    return db_movie


def get_movies(args: schemas.MoviesGetRequest, db: Session) -> list[schemas.MovieBase]:
    filter_fields = {
        Movie.title.key: args.title,
    }

    movie_objects = get_filtered_query(Movie, db.query(Movie), filter_fields).all()
    return [schemas.MovieBase(**item.__dict__) for item in movie_objects]


def get_filtered_query(table, query: Query, filter_fields: dict[str, Any]) -> Query:
    if not filter_fields:
        return query

    for attr, value in filter_fields.items():
        filter_obj = getattr(table, attr, None)
        if filter_obj and value:
            query = query.filter(filter_obj == value)

    return query


def create_movie(movie: schemas.MovieCreate, db: Session):
    movie_title = movie.title.lower()
    movie_exists = db.query(db.query(Movie).filter(Movie.title == movie_title).exists()).scalar()
    if movie_exists:
        raise HTTPException(status_code=400, detail=f"Movie with title - {movie_title} already created")

    db_movie = Movie(
        title=movie_title,
        description=movie.description,
        watched=movie.watched,
        rating=movie.rating)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie_by_id(movie_id: int, movie: schemas.MovieUpdate, db: Session):
    db_movie = get_movie_by_id(movie_id, db)

    for key, value in schemas.MovieUpdate(**movie.__dict__):
        setattr(db_movie, key, value)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie_by_id(movie_id: int, db: Session) -> None:
    db_movie = get_movie_by_id(movie_id, db)
    db.delete(db_movie)
    db.commit()
