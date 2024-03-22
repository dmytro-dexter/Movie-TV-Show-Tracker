from fastapi import HTTPException
from sqlalchemy.orm import Session

from src import schemas, models
from src.query_builder import get_filtered_query, search_query


def get_movie_by_id(movie_id: int, db: Session) -> schemas.MovieBase:
    db_movie = get_filtered_query(models.Movie, db.query(models.Movie), {models.Movie.id.key: movie_id}).first()
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie ID {movie_id} not found")
    return db_movie


def get_movies(args: schemas.MoviesGetRequest, db: Session) -> list[schemas.MovieBase]:
    filter_fields = {
        models.Movie.watched.key: args.watched,
    }
    filtered_movies = get_filtered_query(models.Movie, db.query(models.Movie), filter_fields)
    searched_movies = search_query(
        filtered_movies,
        models.Movie,
        args.search,
        [models.Movie.title.key, models.Movie.id.key],
    )

    movie_objects = searched_movies.all()
    return [schemas.MovieBase(**item.__dict__) for item in movie_objects]


def create_movie(movie: schemas.MovieCreate, db: Session) -> models.Movie:
    movie_exists = db.query(db.query(models.Movie).filter(models.Movie.title == movie.title).exists()).scalar()
    if movie_exists:
        raise HTTPException(status_code=400, detail=f"Movie with title - {movie.title} already created")

    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        watched=movie.watched,
        rating=movie.rating)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie_by_id(movie_id: int, movie: schemas.MovieUpdate, db: Session):
    db_movie = get_movie_by_id(movie_id, db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie with ID {movie_id} does not exist")

    for key, value in schemas.MovieUpdate(**movie.__dict__):
        setattr(db_movie, key, value)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie_by_id(movie_id: int, db: Session) -> None:
    db_movie = get_movie_by_id(movie_id, db)
    if not db_movie:
        raise HTTPException(status_code=400, detail=f"Movie with ID {movie_id} does not exist")
    db.delete(db_movie)
    db.commit()
