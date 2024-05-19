from fastapi import status
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

from abiturient.utils.logger import get_logger
from abiturient.utils.use_case import BaseUseCaseWithSession
from .exceptions import UserAlreadyExists, BaseApplicationException

from abiturient.core.security import verify_password
from abiturient.core.security import hashing_secret
from abiturient.infra.repositories.postgresql.users import UserWriter, UserReader
from abiturient.infra.db.models import User
from abiturient.utils.auth import create_token_pare, AuthTokenPayload
from .schemas import UserResponseSchema, AuthResponseSchema


class RegisterUserUseCase(BaseUseCaseWithSession):
    async def __call__(self, user, *args, **kwargs):
        async with self.session:
            user_writer = UserWriter(session=self.session)
            new_user = User(
                email=user.email,
                password=hashing_secret(user.password)
            )
            try:
                from ..profile.use_cases import CreateUserProfileUseCase
                await user_writer.create_user(new_user)
                await self.session.commit()
                await self.session.refresh(new_user)
                await CreateUserProfileUseCase(session=self.session)(new_user)
                return UserResponseSchema(id=new_user.id, email=new_user.email)

            except IntegrityError as e:
                get_logger().info(msg=f"Attempt to register a user with existing email: {user.email}, Error: {str(e)}")
                await self.session.rollback()
                raise UserAlreadyExists(f"User with email {user.email} already exists.")

            except Exception as e:
                get_logger().info(msg=f"Unexpected error during user registration: {str(e)}")
                await self.session.rollback()
                raise BaseApplicationException(f"Bad request")


class LoginUserUseCase(BaseUseCaseWithSession):
    async def __call__(self, user_login_data, *args, **kwargs):
        async with self.session:
            user_reader = UserReader(self.session)
            user: User | None = await user_reader.get_user_by_email(email=user_login_data.email)

            if user:
                if verify_password(user_login_data.password, user.password):
                    tokens = create_token_pare(
                        AuthTokenPayload(
                            user_id=user.id,
                        )
                    )
                    return AuthResponseSchema(
                        user_id=user.id,
                        email=user.email,
                        **tokens
                    )
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Password is incorrect"}
                )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Login is not exist"}
            )