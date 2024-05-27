from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String
)

from .base import Base


class User(Base):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    profile = relationship('Profile', uselist=False, back_populates='user', lazy='subquery')
    university_reviews = relationship('UniversityReview', back_populates='user')
    educational_program_reviews = relationship('EducationalProgramReview', back_populates='user')
