from fastapi import HTTPException
from sqlalchemy.orm import Session

from src import models, schemas
from src.query_builder import get_filtered_query, search_query


def get_review_by_id(review_id: int, db: Session) -> models.Review:
    db_review = get_filtered_query(models.Review, db.query(models.Review), {models.Review.id.key: review_id}).first()
    if not db_review:
        raise HTTPException(status_code=400, detail=f"Movie ID {review_id} not found")
    return db_review


def get_reviews(args: schemas.ReviewsGetRequest, db: Session) -> list[schemas.ReviewBase]:
    filter_fields = {
        models.Review.movie_id.key: args.movie_id,
    }

    filtered_reviews = get_filtered_query(models.Review, db.query(models.Review), filter_fields)
    searched_reviews = search_query(
        filtered_reviews,
        models.Review,
        args.search,
        [models.Review.text.key, models.Review.movie_id.key, models.Review.id.key, models.Review.title.key]
    )
    return [schemas.ReviewBase(**item.__dict__) for item in searched_reviews]


def create_review(review: schemas.ReviewCreate, movie_id: int, db: Session):
    movie_id_exists = db.query(db.query(models.Movie).filter(models.Movie.id == movie_id).exists()).scalar()
    if not movie_id_exists:
        raise HTTPException(status_code=400, detail=f"Movie ID {movie_id} does not exist")
    db_review = models.Review(
        title=review.title,
        text=review.text,
        movie_id=movie_id,

    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review_by_id(review_id: int, review: schemas.ReviewUpdate, db: Session):
    db_review = get_review_by_id(review_id, db)
    if not db_review:
        raise HTTPException(status_code=400, detail=f"Review with ID {review_id} does not exist")

    for key, value in schemas.ReviewUpdate(**review.__dict__):
        setattr(db_review, key, value)

    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review_by_id(review_id: int, db: Session) -> None:
    db_review = get_review_by_id(review_id, db)
    if not db_review:
        raise HTTPException(status_code=400, detail=f"Review with ID {review_id} does not exist")
    db.delete(db_review)
    db.commit()
