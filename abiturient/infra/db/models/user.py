from .base import Base

from sqlalchemy import (
    Column,
    String
)


class User(Base):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
