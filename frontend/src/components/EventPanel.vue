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

function formatEventDate(value) {
  if (!value || !/^\d{8}$/.test(String(value))) return '일정 미정';

  const date = new Date(`${String(value).slice(0, 4)}-${String(value).slice(4, 6)}-${String(value).slice(6, 8)}T00:00:00`);
  return new Intl.DateTimeFormat('ko-KR', { month: 'short', day: 'numeric' }).format(date);
}

function findEvent(events, contentId) {
  return events.find((event) => String(event.id) === String(contentId));
}

// 게시물에 실려온 축제 정보를 우선 사용하고, 없으면 로드된 이벤트 목록에서 보완한다.
function eventTitle(post, events) {
  return post.content_title || findEvent(events, post.content_id)?.title || null;
}

function eventStart(post, events) {
  return post.content_start_date || findEvent(events, post.content_id)?.eventstartdate || null;
}

function eventEnd(post, events) {
  return post.content_end_date || findEvent(events, post.content_id)?.eventenddate || null;
}

function eventVenue(post, events) {
  return post.content_venue_name || findEvent(events, post.content_id)?.venue_name || null;
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
        </div>

        <p class="post-card-content">{{ post.content }}</p>

        <div class="post-card-footer">
          <span
            v-if="eventVenue(post, events)"
            class="post-card-tag"
          >
            {{ eventVenue(post, events) }}
          </span>
          <span v-if="eventTitle(post, events)" class="post-card-tag">
            🎪 {{ eventTitle(post, events) }}
          </span>
          <span v-if="eventStart(post, events) || eventEnd(post, events)" class="post-card-tag">
            축제 {{ formatEventDate(eventStart(post, events)) }} ~ {{ formatEventDate(eventEnd(post, events)) }}
          </span>
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
