from uuid import uuid4

from sqlalchemy import Boolean, Column, Integer, String, Text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4,
                server_default=func.uuid_generate_v4())
    title = Column(String, index=True)
    description = Column(Text)
    watched = Column(Boolean, default=False)
    rating = Column(Integer)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    reference_users = relationship("User", back_populates="reference_movies")
    reviews = relationship("Review", back_populates="movie")
