from fastapi import FastAPI

from app.chatbot.router import router as chatbot_router
from app.database import Base, engine
from app.post.router import router as post_router
from app.event.router import router as event_router

app = FastAPI(title="VibeMap Backend")
Base.metadata.create_all(bind=engine)

app.include_router(post_router)
app.include_router(chatbot_router)
app.include_router(event_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
