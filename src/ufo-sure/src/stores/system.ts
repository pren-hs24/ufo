import { ref, computed } from "vue";
import { defineStore } from "pinia";
import api from "@/api";

export const useSystemStore = defineStore("system", () => {
    const apiVersion = ref("");
    const isDev = ref(import.meta.env.MODE === "development");
    const uiVersion = computed(() => APP_VERSION + (isDev.value ? " (dev)" : ""));

    (async () => {
        apiVersion.value = await api.system.version();
    })();

    return { apiVersion, uiVersion };
});
