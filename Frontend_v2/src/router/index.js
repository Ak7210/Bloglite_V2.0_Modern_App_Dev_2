import { createRouter, createWebHistory } from "vue-router";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue"),

    },
    {
      path: "/",
      name: "login",
      component: () => import("../views/LoginView.vue"),

    },
    {
      path: "/home",
      name: "Home Page",
      component: () => import("../views/BlogView.vue"),
    },

    {
      path: "/profile",
      name: "User Profile",
      component: () => import("../views/profileView.vue"),
    },
    {
      path: "/summary",
      name: "Show Summary",
      component: () => import("../views/Summary.vue"),
    },

  ],
});

export default router;
