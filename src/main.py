from fastapi import FastAPI

from src.api.routers import register_api
from src.database import engine, Base
from src.misc import description

Base.metadata.create_all(bind=engine)

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
register_api(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
