from fastapi import FastAPI
from .database import Base, engine, get_db
from .routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Costco API",
    description="An API for interacting with Costco items database.",
    version="1.0.0",
)

app.include_router(router)
