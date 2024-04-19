from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4,
                server_default=func.uuid_generate_v4())
    title = Column(String)
    text = Column(Text)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id"))

    movie = relationship("Movie", back_populates="reviews")
