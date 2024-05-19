from typing import Type

from pydantic import BaseModel, UUID4

from abiturient.infra.db.models.profile import StatusEnum
from abiturient.infra.db.models import State


class ProfileUpdateSchema(BaseModel):
    status: StatusEnum | None
    state_id: UUID4 | None


class ProfileResponseSchema(BaseModel):
    user_id: UUID4
    status: StatusEnum | None
    state_id: UUID4 | None
