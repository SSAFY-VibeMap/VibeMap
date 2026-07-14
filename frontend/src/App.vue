<script setup>
import { computed } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

const environmentLabel = computed(() => import.meta.env.VITE_ENV || 'development');
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <RouterLink class="brand" to="/">
        <span class="brand-mark">V</span>
        <span>
          <strong>VibeMap</strong>
          <small>지역 정보 커뮤니티</small>
        </span>
      </RouterLink>

      <nav class="topbar-nav" aria-label="주요 페이지">
        <RouterLink to="/">홈</RouterLink>
        <RouterLink to="/board">게시판</RouterLink>
        <RouterLink to="/events">행사</RouterLink>
      </nav>

      <div class="environment-pill">{{ environmentLabel }}</div>
    </header>

    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>