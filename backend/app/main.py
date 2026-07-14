from fastapi import FastAPI
from .api.events import router as events_router

app = FastAPI(title="MeetEat - Events API")

app.include_router(events_router, prefix="/api/events")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
