import uvicorn

from abiturient.utils.app_start import get_current_app_name
from abiturient.apps.profile.router import profile_router
from abiturient.utils.config_reader import get_config
from abiturient.utils.app_start import get_current_app, connect_app

_APP_NAME = get_current_app_name()

app = get_current_app(docs_url=f"/{_APP_NAME}/docs/", openapi_url=f"/{_APP_NAME}/openapi.json")
connect_app(app, f"/{_APP_NAME}", profile_router)

if __name__ == "__main__":
    uvicorn.run(
        f"abiturient.apps.{_APP_NAME}.__main__:app",
        host="0.0.0.0",
        port=int(get_config().ABITURIENT_PORT)
    )
