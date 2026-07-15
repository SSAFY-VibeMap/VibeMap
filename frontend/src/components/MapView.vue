<script setup>
import { nextTick, onMounted, ref } from "vue";

const props = defineProps({
  markers: { type: Array, default: () => [] },
  selectedEventId: { type: String, default: null },
  onSelectEvent: { type: Function, default: null },
  selectedEvent: { type: Object, default: null },
  onViewEvent: { type: Function, default: null },
});

const mapElement = ref(null);
const mapError = ref("");
let map;

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

onMounted(async () => {
  try {
    const kakao = await loadKakaoMaps();
    kakao.maps.load(async () => {
      await nextTick();
      map = new kakao.maps.Map(mapElement.value, {
        center: new kakao.maps.LatLng(37.5665, 126.978),
        level: 8,
      });
    });
  } catch (error) {
    mapError.value = error.message;
  }
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
