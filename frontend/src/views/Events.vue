<script setup>
import EventPanel from '../components/EventPanel.vue';
import MapView from '../components/MapView.vue';

const sampleEvents = [];
</script>

<template>
  <section class="page page-events">
    <div class="page-header">
      <div>
        <p class="eyebrow">행사</p>
        <h1>지도와 목록의 초기 프레임</h1>
      </div>
      <p>Kakao Map 초기화와 행사 패널을 연결하기 위한 외형을 먼저 구성합니다.</p>
    </div>

    <div class="events-layout">
      <MapView :markers="sampleEvents" />
      <EventPanel :events="sampleEvents" />
    </div>
  </section>
</template>