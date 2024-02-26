from fastapi import FastAPI

import models
from database import engine
from misc import description
from routers import router

models.Base.metadata.create_all(bind=engine)

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
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
