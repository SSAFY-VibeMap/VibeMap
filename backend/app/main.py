from fastapi import FastAPI

from backend.app.chatbot.router import router as chatbot_router
from backend.app.database import Base, engine
from backend.app.post.router import router as post_router

app = FastAPI(title="VibeMap Backend")
Base.metadata.create_all(bind=engine)

app.include_router(post_router)
app.include_router(chatbot_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
