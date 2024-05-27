from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class State(Base):
    __tablename__ = 'state'
    title = Column(String(255), unique=True, nullable=False)

    profiles = relationship('Profile', back_populates='state')
