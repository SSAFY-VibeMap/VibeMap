<script setup>
import { ref } from "vue";
import { RouterLink, RouterView } from "vue-router";

const keyword = ref("");
function search() {
  window.dispatchEvent(new CustomEvent("vibemap-search", { detail: keyword.value }));
}
function createPost() {
  window.dispatchEvent(new CustomEvent("vibemap-create-post"));
}
</script>

<template>
  <div class="app-shell">
    <header class="site-header">
      <RouterLink class="brand" to="/" aria-label="VibeMap 홈">
        <span class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
              d="M12 3v4m0 10v4M5 12H1m22 0h-4M6.2 6.2 3.4 3.4m17.2 17.2-2.8-2.8M6.2 17.8 3.4 20.6m17.2-17.2-2.8 2.8"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
            />
            <path
              d="M12 7.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9Z"
              stroke="currentColor"
              stroke-width="1.8"
            />
          </svg>
        </span>
        <span class="brand-copy">
          <strong>VibeMap</strong>
          <small>서울 행사 지도 · 함께 갈 사람 모집 게시판</small>
        </span>
      </RouterLink>

      <div class="header-actions" aria-label="검색 및 빠른 실행">
        <label class="search-field">
          <span class="search-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle
                cx="11"
                cy="11"
                r="6.5"
                stroke="currentColor"
                stroke-width="1.8"
              />
              <path
                d="m16 16 4.5 4.5"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
              />
            </svg>
          </span>
          <input
            v-model="keyword"
            type="search"
            placeholder="행사·장소·게시글 검색"
            aria-label="행사·장소·게시글 검색"
            @keyup.enter="search"
          />
        </label>

        <button class="header-button header-button-secondary" type="button" @click="search">
          검색
        </button>
        <button class="header-button header-button-primary" type="button" @click="createPost">
          <svg class="button-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" />
          </svg>
          모집 글쓰기
        </button>
      </div>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

  </div>
</template>
