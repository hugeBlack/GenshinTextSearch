import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import("@/pages/HomePage.vue"),
            children: [
                {
                    path: "",
                    name: "homeView",
                    component: () => import("@/views/QueryView.vue"),
                },
                {
                    path: "settings",
                    name: "settingsView",
                    component: () => import("@/views/SettingsView.vue"),
                },
                {
                    path: "talk",
                    name: "talkView",
                    component: () => import("@/views/TalkView.vue"),
                }
            ]
        },

        { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import("@/pages/ErrorPage.vue") },
    ]
})

export default router
