from fastapi import APIRouter

from .views import parse_pdf

ent_router = APIRouter()

ent_router.add_api_route(
    '/pdf',
    parse_pdf,
    methods=['POST'],
)
