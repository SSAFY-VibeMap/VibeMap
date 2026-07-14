<script setup>
defineProps({
  markers: {
    type: Array,
    default: () => [],
  },
});
</script>

<template>
  <section class="panel-card map-card">
    <div class="map-placeholder">
      <p class="eyebrow">지도</p>
      <h3>Kakao Map 초기 영역</h3>
      <p>실제 지도 렌더링은 API 키와 지도 초기화 로직을 연결한 뒤 활성화합니다.</p>
      <div class="tag-row">
        <span class="tag">markers: {{ markers.length }}</span>
        <span class="tag">VITE_KAKAO_MAP_API_KEY</span>
      </div>
    </div>
  </section>
</template>