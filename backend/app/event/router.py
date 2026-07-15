from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from .service import EventService

router = APIRouter()

@router.get("")
def list_events(
    keyword: Optional[str] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    region: str = Query("seoul"),
    category: Optional[str] = Query(None),
):
    # Per project spec, latitude/longitude are required for event listing
    if latitude is None or longitude is None:
        raise HTTPException(status_code=400, detail="latitude and longitude are required")

    service = EventService()
    result = service.list_events(
        region=region,
        keyword=keyword,
        latitude=latitude,
        longitude=longitude,
        page=page,
        limit=limit,
        category=category,
    )
    return result


@router.get("/{event_id}")
def get_event(event_id: str):
    service = EventService()
    ev = service.get_event_by_id(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    return ev
