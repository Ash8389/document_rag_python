from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routes.chat_routes import router as chat_route

app = FastAPI(
    title="Chat service",
    description="This service will be used for getting answers from the LLMs",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://document-rag-frontend-self.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_route)