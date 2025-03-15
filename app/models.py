from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Text,
    DateTime,
    SmallInteger,
    ForeignKey,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    role = Column(
        String(20), default="user", nullable=False
    )  # Options: 'user', 'admin'
