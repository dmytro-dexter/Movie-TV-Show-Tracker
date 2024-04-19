from uuid import uuid4

from sqlalchemy import Boolean, Column, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4,
                server_default=func.uuid_generate_v4())
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    reference_movies = relationship("Movie", back_populates="reference_users")
