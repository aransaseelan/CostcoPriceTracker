from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router

app = FastAPI(
    title="Costco API",
    description="API for tracked Costco items, backed by Neon Postgres price snapshots.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aransaseelan.com",
        "https://www.aransaseelan.com",
        "http://localhost:3000",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(router)
