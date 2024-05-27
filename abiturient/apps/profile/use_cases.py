from abiturient.infra.db.models import Profile
from abiturient.infra.repositories.postgresql.profile import ProfileWriter
from abiturient.utils.use_case import BaseUseCaseWithSession
from abiturient.infra.db.models import User
from .schemas import ProfileResponseSchema


class CreateUserProfileUseCase(BaseUseCaseWithSession):

    async def __call__(self, user, *args, **kwargs):
        async with self.session:
            profile_writer = ProfileWriter(session=self.session)
            profile = Profile(user_id=user.id)
            await profile_writer.create_profile(profile)
            await self.session.commit()
            await self.session.refresh(profile)


class UpdateUserProfileUseCase(BaseUseCaseWithSession):
    async def __call__(self, current_user, profile, *args, **kwargs):
        async with self.session:
            profile_writer = ProfileWriter(self.session)
            await profile_writer.update_profile(id=current_user.profile.id, **profile.model_dump(exclude_unset=True))
            await self.session.commit()
            return ProfileResponseSchema(user_id=current_user.id, **profile.model_dump(exclude_unset=True))


class CreateUniversityReview(BaseUseCaseWithSession):
    ...


class CreateEducationalProgramReview(BaseUseCaseWithSession):
    ...
