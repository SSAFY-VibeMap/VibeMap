<script setup>
import { reactive } from 'vue';

defineProps({
  messages: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['send']);
const form = reactive({ message: '' });

function submitMessage() {
  const text = form.message.trim();
  if (!text) {
    return;
  }

  emit('send', text);
  form.message = '';
}
</script>

<template>
  <section class="panel-card chat-card">
    <header class="chat-header">
      <div>
        <p class="eyebrow">챗봇</p>
        <h3>지역 정보 도우미</h3>
      </div>
      <span class="tag">AI / Rule-based</span>
    </header>

    <div class="chat-history">
      <article v-for="(message, index) in messages" :key="index" :class="['bubble', message.role]">
        <strong>{{ message.role === 'user' ? '나' : 'VibeMap' }}</strong>
        <p>{{ message.content }}</p>
      </article>

      <div v-if="loading" class="bubble assistant">답변을 생성하는 중입니다.</div>
    </div>

    <form class="chat-form" @submit.prevent="submitMessage">
      <input v-model="form.message" type="text" placeholder="예: 강남역 근처 불꽃축제 알려줘" />
      <button class="button button-primary" type="submit">전송</button>
    </form>
  </section>
</template>