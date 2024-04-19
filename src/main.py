from fastapi import FastAPI

from src.api.routers import api_router
from src.apps.router import app_router
from src.database import engine, Base
from src.misc import description

Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def start_application():
    app = FastAPI(
        title="Movie and TV Show Tracker",
        description=description,
        version="0.0.1",
        contact=dict(
            name="Dmytro Boiko the Amazing Programmer",
            url="https://github.com/dmytro-dexter",
            email="dmytroboiko007@gmail.com",
        )
    )
    include_router(app)
    return app


app = start_application()
