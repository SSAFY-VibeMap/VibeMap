<script setup>
import BoardList from '../components/BoardList.vue';
import PostDetail from '../components/PostDetail.vue';
import PostForm from '../components/PostForm.vue';

const samplePosts = [
  {
    id: 1,
    title: '불꽃축제 같이 볼 사람 모집',
    content: '여의도에서 함께 볼 분 구합니다.',
    meet_at: '2026-07-14T10:30',
    region: 'seoul',
    comments: [{ id: 1, content: '저도 참여하고 싶어요!' }],
  },
];
</script>

<template>
  <section class="page page-board">
    <div class="page-header">
      <div>
        <p class="eyebrow">게시판</p>
        <h1>초기 스캐폴딩</h1>
      </div>
      <p>목록, 상세, 작성 폼이 연결될 기본 레이아웃만 먼저 준비했습니다.</p>
    </div>

    <div class="board-layout">
      <BoardList :posts="samplePosts" />
      <PostDetail :post="samplePosts[0]" />
      <PostForm />
    </div>
  </section>
</template>