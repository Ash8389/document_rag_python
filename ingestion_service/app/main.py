from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.ingest_routes import router as ingest_router
from app.kafka.create_topic import create_topic
from app.kafka.config import start_producer, stop_producer


@asynccontextmanager
async def lifespan(app):
    await create_topic()

    await start_producer()

    yield

    await stop_producer()

app = FastAPI(
    title="ingestion_service",
    description="This service is for ingestion of documents",
    version="1.0",
    lifespan=lifespan
)


app.include_router(ingest_router)