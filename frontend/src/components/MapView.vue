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

function moveToCurrentLocation(isInitial = false) {
  if (!navigator.geolocation) {
    if (!isInitial) alert("이 브라우저에서는 위치 정보를 지원하지 않습니다.");
    return;
  }

  // Geolocation API를 통해 현재 위치 좌표를 가져옴
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      const locPosition = new window.kakao.maps.LatLng(lat, lon);
      
      if (map) {
        if (isInitial) {
          map.setCenter(locPosition); // 초기 로드 시에는 애니메이션 없이 즉시 이동
        } else {
          map.panTo(locPosition); // 버튼 클릭 시에는 부드럽게 이동
        }
      }
    },
    (error) => {
      if (!isInitial) {
        console.error("위치 정보를 가져오는데 실패했습니다.", error);
        alert("위치 정보를 가져올 수 없습니다. 권한을 확인해주세요.");
      }
      // 위치 정보를 가져오지 못한 경우 기본값(광화문) 유지
    },
    { enableHighAccuracy: true, timeout: 5000 } // 정확도 향상 및 타임아웃 설정
  );
}

function clearMarkers() {
  kakaoMarkers.forEach((marker) => marker.setMap(null));
  kakaoMarkers = [];
}

function renderMarkers() {
  if (!map || !window.kakao?.maps) return;
  clearMarkers();

  const events = props.markers.filter(validCoordinates);
  if (events.length === 0) return;
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
      moveToCurrentLocation(true);
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
      <button 
        type="button" 
        class="my-location-btn" 
        @click="moveToCurrentLocation()" 
        aria-label="내 현재 위치로 이동"
      >
        🎯 내 위치
      </button>
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

<style scoped>
/* 지도 스테이지에 relative 속성이 있어야 버튼을 맵 내부 우상단에 절대 위치로 띄울 수 있습니다. */
.map-stage {
  position: relative;
}

/* 내 위치 버튼 CSS */
.my-location-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  z-index: 10; /* 카카오맵(보통 z-index가 낮음)보다 위에 노출되도록 설정 */
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.my-location-btn:hover {
  background-color: #f5f5f5;
}
</style>
