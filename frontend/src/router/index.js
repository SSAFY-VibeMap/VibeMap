import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import BoardView from '../views/Board.vue';
import EventsView from '../views/Events.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'VibeMap | 지역 정보 커뮤니티',
    },
  },
  {
    path: '/board',
    name: 'board',
    component: BoardView,
    meta: {
      title: '게시판 | VibeMap',
    },
  },
  {
    path: '/events',
    name: 'events',
    component: EventsView,
    meta: {
      title: '행사 | VibeMap',
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.afterEach((to) => {
  if (to.meta?.title) {
    document.title = to.meta.title;
  }
});

export default router;