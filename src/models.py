from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    watched = Column(Boolean, default=False)
    rating = Column(Integer)
    reviews = Column(String)
