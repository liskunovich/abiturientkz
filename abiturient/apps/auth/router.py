from fastapi import APIRouter

from .views import (
    register_user,
    auth_password_login,
    auth_token_refresh,
    auth_delete_refresh_token
)

auth_router = APIRouter()

auth_router.add_api_route(
    "/users",
    register_user,
    methods=["POST"]
)
auth_router.add_api_route(
    "/password/login",
    auth_password_login,
    methods=["POST"]
)
auth_router.add_api_route(
    "/token/refresh",
    auth_token_refresh,
    methods=["POST"]
)

auth_router.add_api_route(
    "/token/delete",
    auth_delete_refresh_token,
    methods=["POST"]
)
