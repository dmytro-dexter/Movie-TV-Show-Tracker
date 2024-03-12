from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    watched = Column(Boolean, default=False)
    rating = Column(Integer)

    reviews = relationship("Review", back_populates="movie")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    title = Column(String)
    text = Column(Text)
    movie_id = Column(Integer, ForeignKey("movies.id"))

    movie = relationship("Movie", back_populates="reviews")
