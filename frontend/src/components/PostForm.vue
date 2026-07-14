<script setup>
import { reactive } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      title: '',
      content: '',
      password: '',
      content_id: '',
      meet_at: '',
    }),
  },
});

const emit = defineEmits(['submit', 'cancel', 'update:modelValue']);

const form = reactive({ ...props.modelValue });

function handleSubmit() {
  emit('submit', { ...form });
}
</script>

<template>
  <form class="panel-card form-card" @submit.prevent="handleSubmit">
    <div class="form-grid">
      <label>
        <span>제목</span>
        <input v-model="form.title" type="text" placeholder="게시글 제목" />
      </label>

      <label>
        <span>만남 일정</span>
        <input v-model="form.meet_at" type="datetime-local" />
      </label>

      <label class="full-width">
        <span>내용</span>
        <textarea v-model="form.content" rows="6" placeholder="함께할 내용을 작성하세요." />
      </label>

      <label>
        <span>비밀번호</span>
        <input v-model="form.password" type="password" placeholder="수정/삭제용 비밀번호" />
      </label>

      <label>
        <span>연결 ID</span>
        <input v-model="form.content_id" type="text" placeholder="축제 원본 ID" />
      </label>
    </div>

    <div class="form-actions">
      <button class="button button-secondary" type="button" @click="$emit('cancel')">취소</button>
      <button class="button button-primary" type="submit">저장</button>
    </div>
  </form>
</template>