import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import LoginForm from '@/components/LoginForm.vue';
import RegisterBankUser from '@/components/RegisterBankUser.vue';
import ManageBanks from '@/views/ManageBanks.vue';

const routes = [
  { path: '/', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/login', component: LoginForm, meta: { public: true } },
  { path: '/registerBankUser', component: RegisterBankUser, meta: { public: true } },
  { path: '/manageBanks', component: ManageBanks, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !token) return next('/login');
  if (to.path === '/login' && token) return next('/');
  return next();
});

export default router;
