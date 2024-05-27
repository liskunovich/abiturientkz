from fastapi import APIRouter

from .views import update_user_profile, create_university_review, create_educational_program_review

profile_router = APIRouter()

profile_router.add_api_route(
    "/profile",
    update_user_profile,
    methods=["PATCH"]
)

profile_router.add_api_route(
    "/university-reviews",
    create_university_review,
    methods=["POST"]
)

profile_router.add_api_route(
    "/educational-program-reviews",
    create_educational_program_review,
    methods=["GET, POST"]
)
