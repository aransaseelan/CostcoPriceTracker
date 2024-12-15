from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Costco API",
    description="An API for interacting with Costco items database."
)

app.include_router(router)
