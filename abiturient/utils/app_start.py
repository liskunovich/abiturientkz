from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from .patterns import singleton


@singleton
class AbiturientApi(FastAPI):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


def get_current_app(*, docs_url="/docs", openapi_url="/openapi.json") -> AbiturientApi:
    app = AbiturientApi(docs_url=docs_url, openapi_url=openapi_url)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def get_current_app_name() -> str:
    from pathlib import Path
    import inspect
    return Path(inspect.getouterframes(inspect.currentframe(), 2)[1][1]).parent.name


def connect_app(fast_api_object: FastAPI, prefix: str, router: APIRouter):
    fast_api_object.include_router(router=router, prefix=prefix)
