<script setup>
defineProps({
  events: {
    type: Array,
    default: () => [],
  },
});
</script>

<template>
  <section class="panel-card event-panel">
    <header>
      <p class="eyebrow">행사 패널</p>
      <h3>주변 축제 목록</h3>
    </header>

    <ul v-if="events.length" class="event-list">
      <li v-for="event in events" :key="event.id">
        <strong>{{ event.title }}</strong>
        <span>{{ event.venue_name || event.venue_address || '장소 정보 없음' }}</span>
      </li>
    </ul>

    <div v-else class="empty-state">
      축제 데이터를 불러오면 이 패널에 노출됩니다.
    </div>
  </section>
</template>