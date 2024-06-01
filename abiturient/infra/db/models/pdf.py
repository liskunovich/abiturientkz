from __future__ import annotations
import enum

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Table,
    ForeignKey,
    String,
    Integer,
    Enum
)

from .base import Base


class UniversitySpecialization(Base):
    __tablename__ = "university_specialization"
    university_id = Column(ForeignKey("university.id"), primary_key=True)
    specialization_id = Column(ForeignKey("specialization.id"), primary_key=True)
    year_statistics = relationship('YearStatistics', back_populates='university_specialization')


class ConcursEnum(enum.Enum):
    COMMON = 'COMMON'
    RURAL_QUOTA = 'RURAL_QUOTA'


class University(Base):
    __tablename__ = "university"
    code = Column(String(63), unique=True)
    specializations = relationship('Specialization',
                                   secondary=UniversitySpecialization.__tablename__,
                                   back_populates='universities')


class Specialization(Base):
    __tablename__ = "specialization"
    title = Column(String(127), unique=True)
    universities = relationship('University',
                                secondary=UniversitySpecialization.__tablename__,
                                back_populates='specializations')


class YearStatistics(Base):
    __tablename__ = "year_statistics"
    university_specialization_id = Column(ForeignKey("university_specialization.id"))
    university_specialization = relationship('UniversitySpecialization',
                                             back_populates='year_statistics',
                                             uselist=False)

    concurs_type = Column(Enum(ConcursEnum))
    year = Column(Integer())
    students_amount = Column(Integer())
    min_pass_score = Column(Integer())
    max_pass_score = Column(Integer())
    average_pass_score = Column(Integer())
