<script setup>
function formatDateTime(value, includeYear = false) {
  if (!value) return "일정 미정";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat("ko-KR", {
    ...(includeYear ? { year: "numeric" } : {}),
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  }).format(date);
}

defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
  events: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  activePostId: {
    type: [String, Number],
    default: null,
  },
  page: {
    type: Number,
    default: 1,
  },
  pageCount: {
    type: Number,
    default: 1,
  },
  total: {
    type: Number,
    default: null,
  },
});

defineEmits(["select-post", "change-page"]);
</script>

<template>
  <section class="event-panel">
    <div class="section-head">
      <h2>모집 게시판</h2>
      <span class="section-badge">{{ total ?? posts.length }}개 글</span>
    </div>

    <div v-if="loading" class="event-stack">
      <article
        v-for="index in 3"
        :key="index"
        class="event-card event-card-placeholder"
      ></article>
    </div>

    <div v-else-if="posts.length" class="event-stack">
      <button
        v-for="post in posts"
        :key="post.id"
        type="button"
        class="post-card"
        :class="{
          'post-card-active': post.id === activePostId,
        }"
        @click="$emit('select-post', post)"
      >
        <div class="post-card-header">
          <h3 class="post-card-title">{{ post.title }}</h3>
          <span class="section-badge post-count-badge">{{
            post.comments?.length ?? 0
          }}</span>
        </div>

        <p class="post-card-content">{{ post.content }}</p>

        <div class="post-card-footer">
          <span
            v-if="events.find((event) => event.id === post.content_id)"
            class="post-card-tag"
          >
            {{
              events.find((event) => event.id === post.content_id)
                ?.venue_name || "장소 정보 없음"
            }}
          </span>
          <span class="post-card-tag">{{ formatDateTime(post.meet_at) }} 만남</span>
          <span class="post-card-meta">{{ formatDateTime(post.created_at, true) }}</span>
        </div>
      </button>
    </div>

    <div v-else class="event-stack" aria-label="모집 게시판 빈 상태">
      <article
        v-for="index in 3"
        :key="index"
        class="event-card event-card-placeholder"
      ></article>
    </div>

    <nav v-if="pageCount > 1" class="pagination" aria-label="모집 게시글 페이지">
      <button type="button" :disabled="page === 1" aria-label="이전 페이지" @click="$emit('change-page', page - 1)">‹</button>
      <button v-for="number in pageCount" :key="number" type="button" :class="{ active: number === page }" @click="$emit('change-page', number)">{{ number }}</button>
      <button type="button" :disabled="page === pageCount" aria-label="다음 페이지" @click="$emit('change-page', page + 1)">›</button>
    </nav>
  </section>
</template>
