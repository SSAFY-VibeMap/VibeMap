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
        # direct file in data dir
        candidates.append(self.data_dir / f"{region}_축제공연행사.json")
        # special mapping for seoul -> 서울
        if region.lower() == "seoul":
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
                        return json.load(f)
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
        for ev in items:
            if not match(ev):
                continue
            lat = ev.get("latitude") or ev.get("lat")
            lon = ev.get("longitude") or ev.get("lng") or ev.get("lon")
            lat_f = _safe_float(lat)
            lon_f = _safe_float(lon)
            filtered.append({
                "id": str(ev.get("id") or ev.get("content_id") or ev.get("event_id") or ""),
                "title": ev.get("title"),
                "image_url": ev.get("image_url"),
                "venue_name": ev.get("venue_name") or ev.get("place"),
                "venue_address": ev.get("venue_address") or ev.get("addr"),
                "latitude": lat_f,
                "longitude": lon_f,
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
                    arr = json.load(f)
            except Exception:
                continue
            for ev in arr:
                if str(ev.get("id") or ev.get("content_id") or ev.get("event_id")) == str(event_id):
                    return {
                        "id": str(ev.get("id") or ev.get("content_id") or ev.get("event_id") or ""),
                        "title": ev.get("title"),
                        "image_url": ev.get("image_url"),
                        "venue_name": ev.get("venue_name") or ev.get("place"),
                        "venue_address": ev.get("venue_address") or ev.get("addr"),
                        "latitude": ev.get("latitude") or ev.get("lat"),
                        "longitude": ev.get("longitude") or ev.get("lng") or ev.get("lon"),
                        **{k: v for k, v in ev.items() if k not in ["id", "title"]},
                    }
        return None
