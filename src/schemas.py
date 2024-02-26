from pydantic import BaseModel


class MovieCreate(BaseModel):
    title: str
    description: str | None = None
    watched: bool = False
    rating: int | None = None
    reviews: str | None = None


class MovieBase(BaseModel):
    id: int
    title: str
    description: str | None = None
    watched: bool = False
    rating: int | None = None
    reviews: str | None = None


class MovieUpdate(BaseModel):
    title: str
    description: str | None = None
    watched: bool = False
    rating: int | None = None
    reviews: str | None = None
