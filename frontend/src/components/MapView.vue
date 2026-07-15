<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps({
  markers: { type: Array, default: () => [] },
  selectedEventId: { type: String, default: null },
  onSelectEvent: { type: Function, default: null },
  selectedEvent: { type: Object, default: null },
  onViewEvent: { type: Function, default: null },
  // Optional initial center: { latitude, longitude }
  initialCenter: { type: Object, default: null },
});
const emit = defineEmits(["center-changed"]);

const mapElement = ref(null);
const mapError = ref("");
let map;
let kakaoMarkers = [];
let lastCenterEmit = 0;
// Flag set when the user manually interacts (drag/zoom) — prevents auto-centering
let userInteracted = false;
// When true, temporarily prevent auto-fit (used during programmatic pans)
let suppressAutoFit = false;
let programmaticPanTimer = null;
// Ensure auto-fit happens at most once on initial load
let initialAutoFitDone = false;

function validCoordinates(event) {
  return Number.isFinite(Number(event?.latitude)) && Number.isFinite(Number(event?.longitude));
}

function loadKakaoMaps() {
  if (window.kakao?.maps) return Promise.resolve(window.kakao);

  const appKey = import.meta.env.VITE_KAKAO_MAP_JS_KEY;
  if (!appKey) return Promise.reject(new Error("카카오 지도 JavaScript 키가 설정되지 않았습니다."));

  return new Promise((resolve, reject) => {
    const existingScript = document.querySelector("script[data-kakao-map-sdk]");
    if (existingScript) {
      existingScript.addEventListener("load", () => resolve(window.kakao), { once: true });
      existingScript.addEventListener("error", () => reject(new Error("카카오 지도 SDK를 불러올 수 없습니다.")), { once: true });
      return;
    }

    const script = document.createElement("script");
    script.dataset.kakaoMapSdk = "true";
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${encodeURIComponent(appKey)}&autoload=false`;
    script.onload = () => resolve(window.kakao);
    script.onerror = () => reject(new Error("카카오 지도 SDK를 불러올 수 없습니다."));
    document.head.appendChild(script);
  });
}

function clearMarkers() {
  kakaoMarkers.forEach((marker) => marker.setMap(null));
  kakaoMarkers = [];
}

function renderMarkers() {
  if (!map || !window.kakao?.maps) return;
  clearMarkers();

  const events = props.markers.filter(validCoordinates);
  const bounds = new window.kakao.maps.LatLngBounds();
  events.forEach((event) => {
    const position = new window.kakao.maps.LatLng(Number(event.latitude), Number(event.longitude));
    const marker = new window.kakao.maps.Marker({
      map,
      position,
      title: event.title,
      zIndex: event.id === props.selectedEventId ? 2 : 1,
    });
    marker.eventId = event.id;
    window.kakao.maps.event.addListener(marker, "click", () => props.onSelectEvent?.(event));
    kakaoMarkers.push(marker);
    bounds.extend(position);
  });

  // Auto-fit only on initial load and only if not suppressed or user-interacted
  if (!initialAutoFitDone && !userInteracted && !suppressAutoFit) {
    if (events.length > 1) map.setBounds(bounds, 48, 48, 48, 48);
    else if (events.length === 1) map.setCenter(bounds.getSouthWest());
    initialAutoFitDone = true;
  }
}

function focusSelectedEvent() {
  if (!map || !validCoordinates(props.selectedEvent)) return;
  // Programmatic focus: suppress auto-fit briefly while panning
  clearTimeout(programmaticPanTimer);
  suppressAutoFit = true;
  try { map.panTo(new window.kakao.maps.LatLng(Number(props.selectedEvent.latitude), Number(props.selectedEvent.longitude))); } catch (e) {}
  programmaticPanTimer = setTimeout(() => { suppressAutoFit = false; }, 800);
}

function updateSelectedMarker() {
  kakaoMarkers.forEach((marker) => {
    marker.setZIndex(marker.eventId === props.selectedEventId ? 2 : 1);
  });
}

function panToCenter(center) {
  if (!map || !center) return;
  const lat = Number(center.latitude);
  const lng = Number(center.longitude);
  if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
  // suppress auto-fit while programmatically panning, then re-enable
  clearTimeout(programmaticPanTimer);
  suppressAutoFit = true;
  try {
    map.panTo(new window.kakao.maps.LatLng(lat, lng));
  } catch (e) {
    // ignore
  }
  programmaticPanTimer = setTimeout(() => { suppressAutoFit = false; }, 800);
}

defineExpose({ panToCenter });

onMounted(async () => {
  try {
    const kakao = await loadKakaoMaps();
    kakao.maps.load(async () => {
      await nextTick();
      map = new kakao.maps.Map(mapElement.value, {
        center: new kakao.maps.LatLng(37.5665, 126.978),
        level: 8,
      });

      // If parent provided an initial center, apply it
      if (props.initialCenter && Number.isFinite(Number(props.initialCenter.latitude)) && Number.isFinite(Number(props.initialCenter.longitude))) {
        map.setCenter(new kakao.maps.LatLng(Number(props.initialCenter.latitude), Number(props.initialCenter.longitude)));
      }

      // Mark user interaction when dragging or zooming so we avoid auto-centering
      window.kakao.maps.event.addListener(map, "dragstart", () => { userInteracted = true; });
      window.kakao.maps.event.addListener(map, "zoom_changed", () => { userInteracted = true; });

      // Notify parent about center changes (throttled)
      window.kakao.maps.event.addListener(map, "idle", () => {
        try {
          const center = map.getCenter();
          const latitude = center.getLat();
          const longitude = center.getLng();
          const now = Date.now();
          if (now - lastCenterEmit > 400) {
            emit("center-changed", { latitude, longitude });
            lastCenterEmit = now;
          }
        } catch (e) {
          // ignore
        }
      });
      renderMarkers();
    });
  } catch (error) {
    mapError.value = error.message;
  }
});

watch(() => props.markers, renderMarkers, { deep: true });
watch(() => props.selectedEventId, () => {
  updateSelectedMarker();
  focusSelectedEvent();
});
// When parent updates initial center, pan the map (but don't override user's manual view)
watch(() => props.initialCenter, (val) => {
  if (!map || !val) return;
  if (userInteracted) return;
  if (Number.isFinite(Number(val.latitude)) && Number.isFinite(Number(val.longitude))) {
    map.panTo(new window.kakao.maps.LatLng(Number(val.latitude), Number(val.longitude)));
  }
}, { deep: true });
onBeforeUnmount(clearMarkers);

// clear listeners when unmounting
onBeforeUnmount(() => {
  if (map && window.kakao?.maps) {
    try { window.kakao.maps.event.clearListeners(map, 'idle'); } catch (e) { /* ignore */ }
    try { window.kakao.maps.event.clearListeners(map, 'dragstart'); } catch (e) { /* ignore */ }
    try { window.kakao.maps.event.clearListeners(map, 'zoom_changed'); } catch (e) { /* ignore */ }
  }
  try { clearTimeout(programmaticPanTimer); } catch (e) {}
});

</script>

<template>
  <section class="map-card">
    <div class="map-stage">
      <div ref="mapElement" class="kakao-map" aria-label="행사 위치 지도"></div>
      <span v-if="mapError" class="map-warning">{{ mapError }}</span>
      <article v-if="props.selectedEvent" class="selected-event-card map-selected-event">
        <img :src="props.selectedEvent.image_url" :alt="props.selectedEvent.title" class="selected-event-image" />
        <div class="selected-event-copy">
          <p>{{ props.selectedEvent.title }}</p>
          <span>{{ props.selectedEvent.venue_address }}</span>
        </div>
        <button type="button" class="button button-secondary selected-event-button" @click="props.onViewEvent?.(props.selectedEvent)">행사 상세보기</button>
      </article>
    </div>
  </section>
</template>
