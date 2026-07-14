import { createRouter, createWebHistory } from 'vue-router';
import EventsView from '../views/Events.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: EventsView,
    meta: {
      title: 'VibeMap | 서울 축제 동행',
    },
  },
  {
    path: '/events',
    redirect: '/',
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
