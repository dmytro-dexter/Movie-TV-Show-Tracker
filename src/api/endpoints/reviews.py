from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.crud import crud_reviews
from src.schemas import reviews as schemas
from uuid import UUID

router = APIRouter()


@router.get("", response_model=list[schemas.ReviewBase])
def get_all_reviews(
        args: schemas.ReviewsGetRequest = Depends(schemas.ReviewsGetRequest),
        db: Session = Depends(get_db),
) -> list[schemas.ReviewBase]:
    return crud_reviews.get_reviews(args, db)


@router.get("/{review_id}", response_model=schemas.ReviewBase)
def get_review_by_id(review_id: UUID, db: Session = Depends(get_db)) -> schemas.ReviewBase:
    return crud_reviews.get_review_by_id(review_id=review_id, db=db)


@router.post("", response_model=schemas.ReviewBase)
def create_review(review: schemas.ReviewCreate, movie_id: UUID, db: Session = Depends(get_db)) -> schemas.ReviewBase:
    return crud_reviews.create_review(review, movie_id, db)


@router.put("/{review_id}", response_model=schemas.ReviewBase)
def review_update_by_id(review_id: UUID,
                        review: schemas.ReviewUpdate,
                        db: Session = Depends(get_db)) -> schemas.ReviewBase:
    return crud_reviews.update_review_by_id(review_id, review, db)


@router.delete("/{review_id}")
def delete_review_by_id(review_id: UUID, db: Session = Depends(get_db)) -> None:
    crud_reviews.delete_review_by_id(review_id, db)
