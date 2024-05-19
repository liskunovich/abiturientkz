from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from abiturient.infra.db.models import User
from abiturient.utils.auth import get_current_user
from abiturient.infra.db.database import async_session
from abiturient.core.settings import settings_instance

from .schemas import ProfileUpdateSchema, ProfileResponseSchema
from .use_cases import UpdateUserProfileUseCase


async def update_user_profile(
        profile: ProfileUpdateSchema,
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(
            async_session(settings_instance.db_url.unicode_string(), settings_instance))
) -> ProfileResponseSchema:
    user_profile = await UpdateUserProfileUseCase(session)(current_user, profile)
    return user_profile


async def create_university_review(
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(
            async_session(settings_instance.db_url.unicode_string(), settings_instance))
):
    ...


async def create_educational_program_review(
        current_user: User = Depends(get_current_user()),
        session: AsyncSession = Depends(
            async_session(settings_instance.db_url.unicode_string(), settings_instance))
):
    ...
