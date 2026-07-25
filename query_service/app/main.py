from fastapi import FastAPI

from app.routes.chat_routes import router as chat_route

app = FastAPI(
    title="Chat service",
    description="This service will be used for getting answers from the LLMs",
    version="1.0"
)

app.include_router(chat_route)