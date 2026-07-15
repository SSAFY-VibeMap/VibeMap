<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue";
import EventPanel from "../components/EventPanel.vue";
import MapView from "../components/MapView.vue";
import { eventService } from "../services/eventService";

const fallbackEvents = [
  { id: "125678", title: "여의도 한강 불빛축제", image_url: "https://images.unsplash.com/photo-1467810563316-b5476525c0f9?w=800&q=80", venue_name: "여의도 한강공원", venue_address: "서울 영등포구 여의동로 330", latitude: 37.5281, longitude: 126.9346 },
  { id: "125679", title: "서울숲 재즈 페스티벌", image_url: "https://images.unsplash.com/photo-1415201364774-f6f0bb35f28f?w=800&q=80", venue_name: "서울숲", venue_address: "서울 성동구 뚝섬로 273", latitude: 37.5443, longitude: 127.0374 },
  { id: "125680", title: "광화문 빛초롱축제", image_url: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&q=80", venue_name: "광화문광장", venue_address: "서울 종로구 세종대로 172", latitude: 37.5725, longitude: 126.9769 },
  { id: "125681", title: "잠실 롯데 뮤직 페스타", image_url: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800&q=80", venue_name: "잠실종합운동장", venue_address: "서울 송파구 올림픽로 25", latitude: 37.5159, longitude: 127.0731 },
];

const events = ref([]);
const posts = ref([
  { id: 1, title: "불빛축제 같이 보러갈 사람 모집", content: "여의도에서 불빛축제 보고 푸드트럭까지 함께 갈 2명 구합니다!여의도에서 불빛축제 보고 푸드트럭까지 함께 갈 2명 구합니다!여의도에서 불빛축제 보고 푸드트럭까지 함께 갈 2명 구합니다!여의도에서 불빛축제 보고 푸드트럭까지 함께 갈 2명 구합니다!여의도에서 불빛축제 보고 푸드트럭까지 함께 갈 2명 구합니다!", content_id: "125678", meet_at: "2026-07-19T18:00", created_at: "2026-07-14T10:30", comments: [{ id: 1, content: "저도 참여하고 싶어요!", created_at: "2026-07-14T11:00" }], password: "1234" },
  { id: 2, title: "서울숲 재즈 페스티벌 동행 구해요", content: "재즈 좋아하시는 분, 돗자리와 간단한 간식 챙겨 함께 즐겨요.", content_id: "125679", meet_at: "2026-07-20T15:00", created_at: "2026-07-13T09:00", comments: [], password: "1234" },
  { id: 3, title: "광화문 빛초롱축제 야경 같이 보다", content: "사진 찍는 걸 좋아하는 분이면 더 환영합니다.", content_id: "125680", meet_at: "2026-07-21T19:30", created_at: "2026-07-12T20:15", comments: [{ id: 2, content: "카메라 초보인데 괜찮을까요?", created_at: "2026-07-12T21:00" }], password: "1234" },
  ...Array.from({ length: 10 }, (_, index) => {
    const eventIds = ["125681", "125678", "125679", "125680"];
    const number = index + 4;
    return {
      id: number,
      title: `서울 축제 동행 모집 ${number}`,
      content: "행사 관람 후 근처에서 간단히 이야기 나눌 동행을 찾고 있어요.",
      content_id: eventIds[index % eventIds.length],
      meet_at: `2026-07-${String(22 + index).padStart(2, "0")}T${String(13 + (index % 6)).padStart(2, "0")}:00`,
      created_at: `2026-07-${String(11 - Math.min(index, 9)).padStart(2, "0")}T10:00`,
      comments: index % 3 === 0 ? [{ id: 100 + index, content: "함께 참여하고 싶습니다.", created_at: "2026-07-11T11:00" }] : [],
      password: "1234",
    };
  }),
]);
const loading = ref(true);
const selectedEventId = ref(null);
const selectedPostId = ref(null);
const query = ref("");
const currentPage = ref(1);
const postsPerPage = 10;
const detailPost = ref(null);
const eventDetail = ref(null);
const formOpen = ref(false);
const editPost = ref(null);
const deleteOpen = ref(false);
const password = ref("");
const form = reactive({ title: "", content: "", content_id: "", meet_at: "", password: "" });
const schedulePickerOpen = ref(false);
const schedulePickerMonth = ref(new Date());
const schedulePickerStyle = ref({});
const comment = reactive({ content: "", password: "" });
const chatOpen = ref(false);
const chatInput = ref("");
const messages = ref([{ id: "welcome", role: "bot", text: "안녕하세요! 서울 축제 도우미예요. 궁금한 행사나 지역을 물어보세요." }]);

const filteredEvents = computed(() => {
  const keyword = query.value.trim().toLowerCase();
  return keyword ? events.value.filter((event) => `${event.title} ${event.venue_name}`.toLowerCase().includes(keyword)) : events.value;
});
const filteredPosts = computed(() => {
  const keyword = query.value.trim().toLowerCase();
  return keyword ? posts.value.filter((post) => `${post.title} ${post.content}`.toLowerCase().includes(keyword)) : posts.value;
});
const pageCount = computed(() => Math.max(1, Math.ceil(filteredPosts.value.length / postsPerPage)));
const pagedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage;
  return filteredPosts.value.slice(start, start + postsPerPage);
});
const selectedEvent = computed(() => events.value.find((event) => event.id === selectedEventId.value));

function formatDate(value, withYear = false) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("ko-KR", withYear ? { year: "numeric", month: "long", day: "numeric", hour: "2-digit", minute: "2-digit" } : { month: "long", day: "numeric" }).format(date);
}
function toDateKey(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}
function getScheduleDate(value) {
  if (!value) return null;
  const [year, month, day] = value.slice(0, 10).split("-").map(Number);
  return new Date(year, month - 1, day);
}
const scheduleDays = computed(() => {
  const year = schedulePickerMonth.value.getFullYear();
  const month = schedulePickerMonth.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const start = new Date(year, month, 1 - firstDay.getDay());
  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    return { date, key: toDateKey(date), currentMonth: date.getMonth() === month };
  });
});
const scheduleTime = computed({
  get: () => form.meet_at?.slice(11, 16) || "",
  set: (time) => {
    const date = form.meet_at?.slice(0, 10) || toDateKey(new Date());
    form.meet_at = `${date}T${time}`;
  },
});
const scheduleTimes = Array.from({ length: 48 }, (_, index) => {
  const hour = String(Math.floor(index / 2)).padStart(2, "0");
  const minute = index % 2 ? "30" : "00";
  return `${hour}:${minute}`;
});
const scheduleMonthLabel = computed(() => new Intl.DateTimeFormat("ko-KR", { year: "numeric", month: "long" }).format(schedulePickerMonth.value));
function changeScheduleMonth(amount) {
  schedulePickerMonth.value = new Date(schedulePickerMonth.value.getFullYear(), schedulePickerMonth.value.getMonth() + amount, 1);
}
function selectScheduleDate(date) {
  form.meet_at = `${toDateKey(date)}T${scheduleTime.value || "18:00"}`;
  schedulePickerOpen.value = false;
}
function openSchedulePicker(event) {
  const selected = getScheduleDate(form.meet_at) || new Date();
  schedulePickerMonth.value = new Date(selected.getFullYear(), selected.getMonth(), 1);
  schedulePickerOpen.value = !schedulePickerOpen.value;
  if (!schedulePickerOpen.value) return;

  const rect = event.currentTarget.getBoundingClientRect();
  const pickerWidth = 320;
  const pickerHeight = 390;
  const left = Math.min(rect.left, window.innerWidth - pickerWidth - 16);
  const top = rect.bottom + 8 + pickerHeight > window.innerHeight
    ? Math.max(16, rect.top - pickerHeight - 8)
    : rect.bottom + 8;
  schedulePickerStyle.value = { top: `${top}px`, left: `${Math.max(16, left)}px` };
}
function selectEvent(event) { selectedEventId.value = event.id; }
function changePage(page) { currentPage.value = Math.min(Math.max(page, 1), pageCount.value); }
function viewEvent(event) { eventDetail.value = event; }
function openDetail(post) { detailPost.value = post; selectedPostId.value = post.id; if (post.content_id) selectedEventId.value = post.content_id; }
function openForm(post = null) {
  editPost.value = post;
  Object.assign(form, { title: post?.title ?? "", content: post?.content ?? "", content_id: post?.content_id ?? selectedEventId.value ?? "", meet_at: post?.meet_at?.slice(0, 16) ?? "", password: "" });
  schedulePickerOpen.value = false;
  formOpen.value = true;
}
function savePost() {
  if (!form.title.trim() || !form.content.trim() || !form.meet_at || !form.password.trim()) return;
  if (editPost.value) {
    if (editPost.value.password !== form.password) return;
    Object.assign(editPost.value, { title: form.title, content: form.content, meet_at: form.meet_at });
    detailPost.value = editPost.value;
  } else {
    posts.value.unshift({ id: Date.now(), title: form.title, content: form.content, content_id: form.content_id || null, meet_at: form.meet_at, created_at: new Date().toISOString(), comments: [], password: form.password });
  }
  formOpen.value = false;
}
function deletePost() {
  if (!detailPost.value || detailPost.value.password !== password.value) return;
  posts.value = posts.value.filter((post) => post.id !== detailPost.value.id);
  password.value = ""; deleteOpen.value = false; detailPost.value = null;
}
function addComment() {
  if (!comment.content.trim() || !comment.password.trim() || !detailPost.value) return;
  detailPost.value.comments.push({ id: Date.now(), content: comment.content, created_at: new Date().toISOString(), password: comment.password });
  comment.content = ""; comment.password = "";
}
function sendChat() {
  const text = chatInput.value.trim();
  if (!text) return;
  messages.value.push({ id: Date.now(), role: "user", text }); chatInput.value = "";
  const matched = events.value.find((event) => `${event.title} ${event.venue_name}`.includes(text) || text.includes(event.venue_name?.slice(0, 2)));
  messages.value.push({ id: Date.now() + 1, role: "bot", text: matched ? `“${matched.title}” 행사는 ${matched.venue_name}에서 열려요. 지도에서 위치를 확인하고 동행 글도 작성해 보세요.` : "현재 등록된 서울 행사를 찾아볼게요. 여의도, 광화문, 서울숲처럼 지역명을 함께 입력해 주세요." });
}
function receiveSearch(event) { query.value = event.detail ?? ""; currentPage.value = 1; }
function receiveCreate() { openForm(); }

onMounted(async () => {
  window.addEventListener("vibemap-search", receiveSearch);
  window.addEventListener("vibemap-create-post", receiveCreate);
  try {
    const response = await eventService.getEvents({ latitude: 37.5665, longitude: 126.978, limit: 50, region: "seoul" });
    events.value = response?.data?.length ? response.data : fallbackEvents;
  } catch { events.value = fallbackEvents; }
  finally { loading.value = false; }
});
onBeforeUnmount(() => { window.removeEventListener("vibemap-search", receiveSearch); window.removeEventListener("vibemap-create-post", receiveCreate); });
</script>

<template>
  <section class="page page-events">
    <div class="events-layout">
      <section class="map-column">
        <div class="section-head section-head-page">
          <div class="section-head-title"><span class="section-pin" aria-hidden="true">●</span><h1>서울 행사 지도</h1></div>
          <span class="section-badge">{{ filteredEvents.length }}개 행사</span>
        </div>
        <MapView :markers="filteredEvents" :selected-event-id="selectedEventId" :selected-event="selectedEvent" :on-select-event="selectEvent" :on-view-event="viewEvent" />
      </section>
      <EventPanel :posts="pagedPosts" :events="events" :loading="loading" :active-post-id="selectedPostId" :page="currentPage" :page-count="pageCount" :total="filteredPosts.length" @select-post="openDetail" @change-page="changePage" />
    </div>

    <div v-if="eventDetail" class="modal-backdrop" @click.self="eventDetail = null"><article class="modal-card event-detail-modal"><button class="modal-close" type="button" aria-label="닫기" @click="eventDetail = null"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" /></svg></button><img :src="eventDetail.image_url" :alt="eventDetail.title" class="event-detail-image" /><p class="eyebrow">서울 행사</p><h2>{{ eventDetail.title }}</h2><p class="event-detail-place">📍 {{ eventDetail.venue_name }} · {{ eventDetail.venue_address }}</p><div class="modal-footer"><button class="button button-primary" type="button" @click="selectEvent(eventDetail); eventDetail = null; openForm()">이 행사로 모집 글쓰기</button></div></article></div>

    <div v-if="detailPost" class="modal-backdrop" @click.self="detailPost = null">
      <article class="modal-card detail-modal">
        <button class="modal-close" type="button" aria-label="닫기" @click="detailPost = null"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" /></svg></button>
        <h2>{{ detailPost.title }}</h2>
        <button v-if="events.find((event) => event.id === detailPost.content_id)" type="button" class="linked-event" @click="selectEvent(events.find((event) => event.id === detailPost.content_id)); detailPost = null">
          📍 {{ events.find((event) => event.id === detailPost.content_id)?.venue_name }} · 지도에서 위치 보기
        </button>
        <div class="detail-meta"><span>🗓 만남 {{ formatDate(detailPost.meet_at, true) }}</span><span>🕘 작성 {{ formatDate(detailPost.created_at, true) }}</span></div>
        <p class="detail-content">{{ detailPost.content }}</p>
        <div class="detail-actions"><button class="button button-secondary" type="button" @click="openForm(detailPost)">수정</button><button class="button button-danger" type="button" @click="deleteOpen = true">삭제</button></div>
        <section class="comment-section"><h3>💬 댓글 {{ detailPost.comments.length }}</h3><div v-for="item in detailPost.comments" :key="item.id" class="comment-item"><p>{{ item.content }}</p><span>{{ formatDate(item.created_at, true) }}</span></div><p v-if="!detailPost.comments.length" class="muted">아직 댓글이 없습니다. 첫 댓글을 남겨 보세요.</p><textarea v-model="comment.content" rows="2" placeholder="댓글을 입력하세요"></textarea><div class="comment-form"><input v-model="comment.password" type="password" placeholder="비밀번호" /><button class="button button-primary" type="button" @click="addComment">댓글 등록</button></div></section>
      </article>
    </div>

    <div v-if="formOpen" class="modal-backdrop" @click.self="formOpen = false"><form class="modal-card form-modal" @submit.prevent="savePost"><button class="modal-close" type="button" aria-label="닫기" @click="formOpen = false"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" /></svg></button><h2>{{ editPost ? '게시글 수정' : '함께 갈 사람 모집' }}</h2><p class="muted">축제를 함께 즐길 동행을 모집하는 글을 작성해 보세요.</p><label>제목<input v-model="form.title" placeholder="예: 불빛축제 같이 보러갈 사람 모집" /></label><label v-if="!editPost">연결된 축제<select v-model="form.content_id"><option value="">연결 안 함</option><option v-for="event in events" :key="event.id" :value="event.id">{{ event.title }}</option></select></label><label>내용<textarea v-model="form.content" rows="4" placeholder="모집 인원, 만날 장소, 준비물을 적어주세요."></textarea></label><label>만남 일정<div class="schedule-picker"><button type="button" class="schedule-trigger" :class="{ 'schedule-trigger-empty': !form.meet_at }" @click="openSchedulePicker"><span>🗓</span>{{ form.meet_at ? formatDate(form.meet_at, true) : '날짜와 시간을 선택하세요' }}</button><div v-if="schedulePickerOpen" class="schedule-popover"><div class="schedule-calendar-head"><button type="button" aria-label="이전 달" @click="changeScheduleMonth(-1)">‹</button><strong>{{ scheduleMonthLabel }}</strong><button type="button" aria-label="다음 달" @click="changeScheduleMonth(1)">›</button></div><div class="schedule-weekdays"><span v-for="day in ['일', '월', '화', '수', '목', '금', '토']" :key="day">{{ day }}</span></div><div class="schedule-days"><button v-for="day in scheduleDays" :key="day.key" type="button" :class="{ muted: !day.currentMonth, selected: form.meet_at?.startsWith(day.key), today: day.key === toDateKey(new Date()) }" @click="selectScheduleDate(day.date)">{{ day.date.getDate() }}</button></div><label class="schedule-time">시간<select v-model="scheduleTime"><option value="" disabled>시간 선택</option><option v-for="time in scheduleTimes" :key="time" :value="time">{{ time }}</option></select></label></div></div></label><label>비밀번호<input v-model="form.password" type="password" placeholder="수정/삭제 때 사용할 비밀번호" /></label><div class="modal-footer"><button class="button button-secondary" type="button" @click="formOpen = false">취소</button><button class="button button-primary" type="submit">{{ editPost ? '수정하기' : '등록하기' }}</button></div></form></div>

    <div v-if="deleteOpen" class="modal-backdrop" @click.self="deleteOpen = false"><form class="modal-card password-modal" @submit.prevent="deletePost"><h2>게시글 삭제</h2><p class="muted">작성할 때 입력한 비밀번호를 입력하세요.</p><input v-model="password" type="password" autofocus placeholder="비밀번호" /><div class="modal-footer"><button class="button button-secondary" type="button" @click="deleteOpen = false">취소</button><button class="button button-danger" type="submit">삭제</button></div></form></div>

    <button class="chat-fab" :class="{ 'chat-fab-open': chatOpen }" type="button" :aria-label="chatOpen ? '채팅 닫기' : '채팅 열기'" @click="chatOpen = !chatOpen"><svg v-if="chatOpen" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" /></svg><svg v-else viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 15.5A4.5 4.5 0 0 1 15.5 20H9l-5 3v-3.7A4.5 4.5 0 0 1 1 15.5v-8A4.5 4.5 0 0 1 5.5 3h10A4.5 4.5 0 0 1 20 7.5v8Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" /></svg></button>
    <section v-if="chatOpen" class="chat-window"><header><strong>축제 도우미</strong><span>AI 챗봇</span></header><div class="chat-messages"><p v-for="message in messages" :key="message.id" :class="['chat-message', message.role]">{{ message.text }}</p></div><form class="chat-input" @submit.prevent="sendChat"><input v-model="chatInput" placeholder="메시지를 입력하세요" /><button class="button button-primary" type="submit">전송</button></form></section>
  </section>
</template>
