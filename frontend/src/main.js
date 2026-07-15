import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './styles/main.css';
import { Toaster } from "vue-sonner";
import "vue-sonner/style.css";

createApp(App).use(router).mount('#app');