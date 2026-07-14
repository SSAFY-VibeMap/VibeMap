<script setup>
defineProps({
  posts: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
  emptyMessage: {
    type: String,
    default: '게시글이 아직 없습니다.',
  },
});

defineEmits(['select']);
</script>

<template>
  <section class="panel-stack">
    <div v-if="loading" class="empty-state">게시글을 불러오는 중입니다.</div>

    <button
      v-for="post in posts"
      :key="post.id"
      type="button"
      class="board-item"
      @click="$emit('select', post)"
    >
      <strong>{{ post.title }}</strong>
      <p>{{ post.content }}</p>
      <span>{{ post.meet_at || '만남 일정 미정' }}</span>
    </button>

    <div v-if="!loading && !posts.length" class="empty-state">
      {{ emptyMessage }}
    </div>
  </section>
</template>