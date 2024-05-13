if __name__ == "__main__":
    import uvicorn
    from abiturient.utils.app_start import get_current_app

    from fastapi import FastAPI

    app: FastAPI = get_current_app()

    config = uvicorn.Config(
        app,
        host='0.0.0.0',
    )
    uvicorn_server = uvicorn.Server(config)
