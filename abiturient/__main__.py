from abiturient.utils.config_reader import get_config

if __name__ == "__main__":
    import uvicorn
    from abiturient.utils.app_start import get_current_app, connect_app
    from apps.about.router import about_router
    from apps.auth.router import auth_router
    from apps.profile.router import profile_router
    from apps.ent.router import ent_router

    from fastapi import FastAPI

    app: FastAPI = get_current_app()
    connect_app(app, '/about', about_router)
    connect_app(app, '/auth', auth_router)
    connect_app(app, '/profile', profile_router)
    connect_app(app, '/ent', ent_router)
    config = uvicorn.Config(
        app,
        host='0.0.0.0',
        port=int(get_config().ABITURIENT_PORT)
    )
    uvicorn_server = uvicorn.Server(config)

