import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.chatbot.router import router as chatbot_router
from app.database import Base, engine
from app.post.router import router as post_router

app = FastAPI(title="VibeMap Backend")
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, frontend_url.replace("localhost", "127.0.0.1")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(post_router)
app.include_router(chatbot_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
