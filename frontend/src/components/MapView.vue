<script setup>
const props = defineProps({
  markers: {
    type: Array,
    default: () => [],
  },
  selectedEventId: {
    type: String,
    default: null,
  },
  onSelectEvent: {
    type: Function,
    default: null,
  },
  selectedEvent: {
    type: Object,
    default: null,
  },
  onViewEvent: {
    type: Function,
    default: null,
  },
});

const bounds = {
  minLat: 37.44,
  maxLat: 37.7,
  minLng: 126.82,
  maxLng: 127.18,
};

function toPercent(value, min, max) {
  const range = max - min;
  if (!range) return 0;
  return ((value - min) / range) * 100;
}

function getMarkerPosition(marker, index) {
  const lat = Number(marker.latitude);
  const lng = Number(marker.longitude);

  if (Number.isFinite(lat) && Number.isFinite(lng)) {
    return {
      left: `${toPercent(lng, bounds.minLng, bounds.maxLng)}%`,
      top: `${100 - toPercent(lat, bounds.minLat, bounds.maxLat)}%`,
    };
  }

  return {
    left: `${12 + (index % 8) * 10}%`,
    top: `${18 + Math.floor(index / 8) * 12}%`,
  };
}
</script>

<template>
  <section class="map-card">
    <div class="map-stage">
      <span class="map-warning">⚠ 카카오 키 미설정 — 대체 지도</span>
      <div class="map-grid" aria-hidden="true"></div>
      <div v-if="props.markers.length" class="map-markers">
        <button
          v-for="(marker, index) in props.markers.slice(0, 12)"
          :key="marker.id"
          type="button"
          class="map-marker"
          :class="{ 'map-marker-active': marker.id === props.selectedEventId }"
          :style="getMarkerPosition(marker, index)"
          @click="props.onSelectEvent?.(marker)"
        ></button>
      </div>
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
