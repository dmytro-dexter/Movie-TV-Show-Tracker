from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel


class ReviewCreate(BaseModel):
    title: str | None = None
    text: str


class ReviewBase(BaseModel):
    id: int
    title: str | None = None
    text: str

    class Config:
        orm_mode = True


class ReviewUpdate(BaseModel):
    title: str | None = None
    text: str


@dataclass
class ReviewsGetRequest:
    limit: int = Query(50, ge=1, le=100, description="The numbers of items to return.")
    offset: int = Query(0, ge=0, description="The number of items to skip before returning the result set.")
    search: str | None = Query("", description="Search by Review Title or ID.")
    movie_id: int | None = Query(None, description="Search reviews by Movie")
