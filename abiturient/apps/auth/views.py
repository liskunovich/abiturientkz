from fastapi import Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from abiturient.infra.db.database import async_session
from abiturient.core.settings import settings_instance
from abiturient.infra.db.models import User
from abiturient.infra.repositories.postgresql.users import UserWriter, UserReader
from abiturient.core.security import hashing_secret, verify_password
from abiturient.utils.auth import delete_refresh_token, create_token_pare, AuthTokenPayload, rotate_refresh_token, \
    create_access_token
from .exceptions import UserAlreadyExists
from .schemas import UserCreateSchema, UserResponseSchema, UserLoginSchema, AuthResponseSchema, UserPasswordLoginSchema


async def register_user(user: UserCreateSchema,
                        session: AsyncSession = Depends(
                            async_session(settings_instance.db_url.unicode_string(), settings_instance))
                        ) -> UserResponseSchema:
    async with session:
        user_writer = UserWriter(session=session)
        new_user = User(
            email=user.email,
            password=hashing_secret(user.password)
        )
        try:
            await user_writer.create_user(new_user)
            await session.commit()
            await session.refresh(new_user)
            return UserResponseSchema(id=new_user.id, email=new_user.email)
        except:
            await session.rollback()
            raise UserAlreadyExists()


async def auth__password_login(
        user_login_data: UserPasswordLoginSchema,
        session: AsyncSession = Depends(
            async_session(settings_instance.db_url.unicode_string(), settings_instance))

) -> AuthResponseSchema:
    """Authentication by login and password"""
    async with session:
        user_reader = UserReader(session)
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


async def auth__token_refresh(
        _auth_obj: tuple[User, str] = Depends(rotate_refresh_token)
) -> AuthResponseSchema:
    user = _auth_obj[0]

    payload = AuthTokenPayload(
        user_id=user.id,
    )

    return AuthResponseSchema(
        user_id=user.id,
        email=user.email,
        access_token=create_access_token(payload),
        refresh_token=_auth_obj[1]
    )


async def auth_delete_refresh_token(
        _curr_user: User = Depends(delete_refresh_token)
) -> JSONResponse:
    return JSONResponse(
        content={"detail": "Refresh tokens was deleted"},
        status_code=200
    )
