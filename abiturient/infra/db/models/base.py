import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import as_declarative
from sqlalchemy.dialects.postgresql import UUID


@as_declarative()
class Base:
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        index=True,
        unique=True
    )
    created_at = Column(
        DateTime,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime
    )
