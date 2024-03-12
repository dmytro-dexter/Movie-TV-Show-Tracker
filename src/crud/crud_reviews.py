from typing import Any

from fastapi import HTTPException, Query
from sqlalchemy.orm import Session

from src.models.models_movies import Review
from src.schemas import reviews as schemas


def get_filtered_query(table, query: Query, filter_fields: dict[str, Any]) -> Query:
    if not filter_fields:
        return query

    for attr, value in filter_fields.items():
        filter_obj = getattr(table, attr, None)
        if filter_obj and value:
            query = query.filter(filter_obj == value)

    return query


def get_review_by_id(review_id: int, db: Session) -> Review:
    db_review = get_filtered_query(Review, db.query(Review), {Review.id.key: review_id}).first()
    if not db_review:
        raise HTTPException(status_code=400, detail=f"Movie ID {review_id} not found")
    return db_review


def get_reviews(args: schemas.ReviewsGetRequest, db: Session) -> list[schemas.ReviewBase]:
    filter_fields = {
        Review.title.key: args.search,
    }

    review_objects = get_filtered_query(Review, db.query(Review), filter_fields).all()
    return [schemas.ReviewBase(**item.__dict__) for item in review_objects]


def create_review(review: schemas.ReviewCreate, movie_id: int, db: Session):
    db_review = Review(
        text=review.text,
        movie_id=movie_id,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review_by_id(review_id: int, review: schemas.ReviewUpdate, db: Session):
    db_review = get_review_by_id(review_id, db)

    for key, value in schemas.ReviewUpdate(**review.__dict__):
        setattr(db_review, key, value)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review_by_id(review_id: int, db: Session) -> None:
    db_review = get_review_by_id(review_id, db)
    db.delete(db_review)
    db.commit()
