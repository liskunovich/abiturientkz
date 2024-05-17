from fastapi import APIRouter

from .views import (
    about__get_current_version,
)

about_router = APIRouter()

about_router.add_api_route(
    "/version",
    about__get_current_version,
    methods=["GET"]
)
