from fastapi import FastAPI

from .routers import router

app = FastAPI(
    title="Costco API",
    description="An API for interacting with Costco items (in-memory, no database).",
)

app.include_router(router)
