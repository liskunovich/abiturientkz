from sqlalchemy import Column, Integer, ForeignKey, UUID, Text
from sqlalchemy.orm import relationship

from .base import Base


class Review(Base):  # TODO: Подумать над добавлением фотографий к отзыву.
    __abstract__ = True
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    text = Column(Text(), nullable=False)


class UniversityReview(Review):  # TODO: Добавить отношения к модели университа.
    __tablename__ = 'university_review'
    user = relationship("User", back_populates="university_reviews")


class EducationalProgramReview(Review):  # TODO: Добавить отношения к модели ОП.
    __tablename__ = 'educational_program_review'
    user = relationship("User", back_populates="educational_program_reviews")
