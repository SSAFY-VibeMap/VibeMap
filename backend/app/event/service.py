import json
import math
from pathlib import Path
from typing import Optional, Dict, Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


class EventService:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DATA_DIR

    def _load_region_file(self, region: str):
        # Try multiple strategies to locate region JSON (support en/kr names and nested folders)
        candidates = []
        candidates.append(self.data_dir / "서울_축제공연행사.json")
        # nested folder: data/<region>/*.json
        nested_dir = self.data_dir / region
        if nested_dir.exists() and nested_dir.is_dir():
            for p in nested_dir.glob("*.json"):
                candidates.append(p)

        for c in candidates:
            if c.exists():
                try:
                    with open(c, encoding="utf-8") as f:
                        data = json.load(f)
                        # unwrap common wrapper that contains items list
                        if isinstance(data, dict) and "items" in data and isinstance(data["items"], list):
                            return data["items"]
                        return data
                except Exception:
                    continue

        # fallback: search any json file whose filename contains region or '서울' when region=seoul
        for p in self.data_dir.rglob("*.json"):
            name = p.name.lower()
            if region.lower() in name or (region.lower() == "seoul" and "서울" in p.name):
                try:
                    with open(p, encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    continue

        return []

    def list_events(self, region: str = "seoul", keyword: Optional[str] = None, page: int = 1, limit: int = 10, category: Optional[str] = None, latitude: Optional[float] = None, longitude: Optional[float] = None) -> Dict[str, Any]:
        items = self._load_region_file(region)

        # Normalize items: ensure keys exist
        def match(ev):
            if keyword:
                kw = keyword.lower()
                if kw not in str(ev.get("title", "")).lower() and kw not in str(ev.get("venue_name", "")).lower():
                    return False
            if category:
                if ev.get("category") and category not in ev.get("category"):
                    return False
            return True

        def _safe_float(val):
            try:
                if val is None or val == "":
                    return None
                return float(val)
            except Exception:
                return None

        filtered = []
        # if file contained a top-level object, ensure we iterate the list of events
        if isinstance(items, dict) and "items" in items:
            items = items.get("items") or []

        for ev in items:
            if not match(ev):
                continue
            # id candidates: several source files use different keys
            id_val = ev.get("id") or ev.get("contentid") or ev.get("content_id") or ev.get("event_id")

            # coordinate candidates: mapy=latitude, mapx=longitude in provided JSON
            lat = ev.get("latitude") or ev.get("lat") or ev.get("mapy") or ev.get("map_y")
            lon = ev.get("longitude") or ev.get("lng") or ev.get("lon") or ev.get("mapx") or ev.get("map_x")
            lat_f = _safe_float(lat)
            lon_f = _safe_float(lon)

            # image fields in source data
            image = ev.get("image_url") or ev.get("firstimage") or ev.get("firstimage2")

            # address fields
            addr = ev.get("venue_address") or ev.get("addr") or ev.get("addr1")

            start_raw = ev.get("eventstartdate") or ev.get("startdate") or ev.get("event_start_date") or ev.get("start_date")
            end_raw = ev.get("eventenddate") or ev.get("enddate") or ev.get("event_end_date") or ev.get("end_date")

            filtered.append({
                "id": str(id_val or ""),
                "title": ev.get("title"),
                "image_url": image,
                "venue_name": ev.get("venue_name") or ev.get("place") or ev.get("title"),
                "venue_address": addr,
                "latitude": lat_f,
                "longitude": lon_f,
                "eventstartdate": str(start_raw) if start_raw not in (None, "") else None,
                "eventenddate": str(end_raw) if end_raw not in (None, "") else None,
            })

        # If latitude/longitude provided, compute haversine distance and sort by it
        def _haversine_m(lat1, lon1, lat2, lon2):
            # returns distance in meters, or None if inputs invalid
            try:
                if None in (lat1, lon1, lat2, lon2):
                    return None
                # convert degrees to radians
                phi1 = math.radians(lat1)
                phi2 = math.radians(lat2)
                dphi = math.radians(lat2 - lat1)
                dlambda = math.radians(lon2 - lon1)
                a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                R = 6371000.0
                return R * c
            except Exception:
                return None

        if latitude is not None and longitude is not None:
            for it in filtered:
                it["distance"] = _haversine_m(latitude, longitude, it.get("latitude"), it.get("longitude"))
            # sort: items with valid distance first, ascending; missing distances go to the end
            filtered.sort(key=lambda x: x.get("distance") if x.get("distance") is not None else float("inf"))

        total = len(filtered)
        total_page = math.ceil(total / limit) if limit else 1
        start = (page - 1) * limit
        end = start + limit
        page_items = filtered[start:end]

        return {
            "data": page_items,
            "total_page": total_page,
            "page": page,
            "limit": limit,
        }

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        # search across region files
        # scan data_dir for json files
        for p in self.data_dir.rglob("*.json"):
            try:
                with open(p, encoding="utf-8") as f:
                    raw = json.load(f)
            except Exception:
                continue
            # normalize to a list of event dicts
            if isinstance(raw, dict):
                if "items" in raw and isinstance(raw["items"], list):
                    arr = raw["items"]
                else:
                    arr = [raw]
            elif isinstance(raw, list):
                arr = raw
            else:
                # unexpected type -> skip
                arr = []

            for ev in arr:
                # support multiple id key names
                ev_id = ev.get("id") or ev.get("contentid") or ev.get("content_id") or ev.get("event_id")
                if str(ev_id) == str(event_id):
                    # normalize returned fields
                    id_val = ev_id
                    image = ev.get("image_url") or ev.get("firstimage") or ev.get("firstimage2")
                    addr = ev.get("venue_address") or ev.get("addr") or ev.get("addr1")
                    lat = ev.get("latitude") or ev.get("lat") or ev.get("mapy")
                    lon = ev.get("longitude") or ev.get("lng") or ev.get("lon") or ev.get("mapx")
                    
                    start_raw = ev.get("eventstartdate") or ev.get("startdate") or ev.get("event_start_date") or ev.get("start_date")
                    end_raw = ev.get("eventenddate") or ev.get("enddate") or ev.get("event_end_date") or ev.get("end_date")
                    
                    return {
                        "id": str(id_val or ""),
                        "title": ev.get("title"),
                        "image_url": image,
                        "venue_name": ev.get("venue_name") or ev.get("place") or ev.get("title"),
                        "venue_address": addr,
                        "latitude": lat,
                        "longitude": lon,
                        "eventstartdate": str(start_raw) if start_raw not in (None, "") else None,
                        "eventenddate": str(end_raw) if end_raw not in (None, "") else None,                   
                    }
        return None
