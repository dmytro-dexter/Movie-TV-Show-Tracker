from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel, Field
from src.schemas.reviews import ReviewBase


class MovieCreate(BaseModel):
    title: str
    description: str | None = None
    watched: bool = False
    rating: int | None = Field(None, qe=1, le=5)


class MovieBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    watched: bool = False
    rating: int | None = Field(None, qe=1, le=5)

    reviews: list[ReviewBase] | None = []

    class Config:
        orm_mode = True


class MovieUpdate(BaseModel):
    title: str
    description: str | None = None
    watched: bool = False
    rating: int | None = Field(None, qe=1, le=5)


@dataclass
class MoviesGetRequest:
    limit: int = Query(50, ge=1, le=100, description="The numbers of items to return.")
    offset: int = Query(0, ge=0, description="The number of items to skip before returning the result set.")
    search: str | None = Query("", description="Search by Movie Title or ID.")
    watched: bool | None = Query(None, description="Filter by Movie Title.")
