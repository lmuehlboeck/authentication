import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import RegisterSuccessView from '../views/RegisterSuccessView.vue'
import UserView from '../views/UserView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      title: 'Login - Authentication byLeo'
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      title: 'Registrieren - Authentication byLeo'
    }
  },
  {
    path: '/register/success',
    name: 'success',
    component: RegisterSuccessView,
    meta: {
      title: 'Registrierung erfolgreich'
    }
  },
  {
    path: '/',
    name: 'user',
    component: UserView,
    meta: {
      title: 'Mein Benutzer'
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const title = to.meta.title
  if (title) {
    document.title = title
  }
  next()
})

export default router
