import { createRouter, createWebHashHistory } from "vue-router";

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: () => import("../views/HomeView.vue"),
        },
        {
            path: "/script",
            name: "script-runner",
            component: () => import("../views/ScriptRunnerView.vue"),
        },
        {
            path: "/logger",
            name: "logger",
            component: () => import("../views/LoggerView.vue"),
        },
        ,
        {
            path: "/settings",
            name: "settings",
            component: () => import("../views/SettingsView.vue"),
        },
    ],
});

export default router;
