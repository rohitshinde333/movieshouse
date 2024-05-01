import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/movies',
    name: 'movies',
    component: () => import('../components/MovieList.vue')
  },
  {
    path: '/',
    name: 'LoginSignUp',
    component: () => import('../views/LoginSignupView.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../components/UserHome.vue')
  },
  {
    path: '/AdminHome',
    name: 'AdminHome',
    component: () => import('../components/AdminHome.vue')
  },
  {
    path: '/MoviePage/:movieId',
    name: 'MoviePage',
    component: () => import('../components/MoviePage.vue')
  },
  {
    path: '/TheatreAdminHome',
    name: 'TheatreAdminHome',
    component: () => import('../components/TheatreAdminHome.vue')
  },
  {
    path: '/TheatreAdminRequest',
    name: 'TheatreAdminRequest',
    component: () => import('../components/TheatreAdminRequest.vue')
  },
  {
    path: '/Theaters',
    name: 'Theaters',
    component: () => import('../components/Theaters.vue')
  },
  {
    path: '/theater/:theaterId',
    name: 'theater-show',
    component: () => import('../components/ShowsAtTheater.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router;
