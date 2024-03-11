from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.crud import crud_reviews
from src.schemas import reviews

router = APIRouter()


@router.get("", response_model=list[reviews.ReviewBase])
def get_all_reviews(
        args: reviews.ReviewsGetRequest = Depends(reviews.ReviewsGetRequest),
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = 50,
) -> list[reviews.ReviewBase]:
    return crud_reviews.get_reviews(args, offset, limit, db)


@router.get("/{review_id}", response_model=reviews.ReviewBase)
def get_review_by_id(review_id: int, db: Session = Depends(get_db)) -> reviews.ReviewBase:
    return crud_reviews.get_review_by_id(review_id=review_id, db=db)


@router.post("", response_model=reviews.ReviewBase)
def create_review(review: reviews.ReviewCreate, movie_id: int, db: Session = Depends(get_db)) -> reviews.ReviewBase:
    return crud_reviews.create_review(review, movie_id, db)


@router.put("/reviews/{review_id}", response_model=reviews.ReviewBase)
def review_update_by_id(review_id: int,
                        review: reviews.ReviewUpdate,
                        db: Session = Depends(get_db)) -> reviews.ReviewBase:
    return crud_reviews.update_review_by_id(review_id, review, db)


@router.delete("/review/{review_id}")
def delete_review_by_id(review_id: int, db: Session = Depends(get_db)) -> None:
    crud_reviews.delete_review_by_id(review_id, db)
