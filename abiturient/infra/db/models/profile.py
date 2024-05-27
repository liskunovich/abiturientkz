import enum

from sqlalchemy import Column, ForeignKey, Integer, UUID, Enum
from sqlalchemy.orm import relationship

from .base import Base


class StatusEnum(enum.Enum):
    SCHOOLKID = 'School Kid'
    STUDENT = 'Student'
    WORKER = 'Worker'


class Profile(Base):
    __tablename__ = 'profile'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='profile')
    status = Column(Enum(StatusEnum))

    state_id = Column(UUID(as_uuid=True), ForeignKey('state.id'), nullable=True)
    state = relationship('State', back_populates='profiles')
