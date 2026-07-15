<script setup>
defineProps({
  post: {
    type: Object,
    default: null,
  },
});
</script>

<template>
  <article v-if="post" class="panel-card detail-card">
    <header class="detail-header">
      <div>
        <p class="eyebrow">게시글 상세</p>
        <h2>{{ post.title }}</h2>
      </div>
    </header>

    <p class="detail-meta">{{ post.meet_at || '만남 일정 미정' }}</p>
    <p class="detail-content">{{ post.content }}</p>

    <section v-if="post.comments?.length" class="comment-block">
      <h3>댓글</h3>
      <ul>
        <li v-for="comment in post.comments" :key="comment.id">
          <strong>익명</strong>
          <p>{{ comment.content }}</p>
        </li>
      </ul>
    </section>
  </article>

  <section v-else class="panel-card empty-state">
    게시글을 선택하면 상세 내용을 확인할 수 있습니다.
  </section>
</template>
