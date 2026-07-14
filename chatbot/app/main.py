from fastapi import FastAPI

from app.chatbot.router import router as chatbot_router

app = FastAPI(title="VibeMap Backend")
app.include_router(chatbot_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
