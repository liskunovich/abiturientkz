from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from abiturient.infra.db.database import async_session
from abiturient.core.settings import settings_instance
from abiturient.infra.db.models import User
from abiturient.utils.auth import delete_refresh_token, create_token_pare, AuthTokenPayload, rotate_refresh_token, \
    create_access_token
from .schemas import UserCreateSchema, UserResponseSchema, UserLoginSchema, AuthResponseSchema, UserPasswordLoginSchema
from .use_cases import RegisterUserUseCase, LoginUserUseCase


async def register_user(user: UserCreateSchema,
                        session: AsyncSession = Depends(
                            async_session(settings_instance.db_url.unicode_string(), settings_instance))
                        ) -> UserResponseSchema:
    user = await RegisterUserUseCase(session)(user=user)
    return user


async def auth_password_login(
        user_login_data: UserPasswordLoginSchema,
        session: AsyncSession = Depends(
            async_session(settings_instance.db_url.unicode_string(), settings_instance))

) -> AuthResponseSchema:
    """Authentication by login and password"""
    user = await LoginUserUseCase(session)(user_login_data=user_login_data)
    return user


async def auth_token_refresh(
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
