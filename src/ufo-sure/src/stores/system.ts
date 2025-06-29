import { ref, computed } from "vue";
import { defineStore } from "pinia";
import api from "@/api";

export const useSystemStore = defineStore("system", () => {
    const algorithm = ref<string | null>(null);
    const apiVersion = ref("");
    const isDev = ref(import.meta.env.MODE === "development");
    const uiVersion = computed(() => APP_VERSION + (isDev.value ? " (dev)" : ""));

    (async () => {
        apiVersion.value = await api.system.version();
        algorithm.value = await api.system.algorithm();
    })();

    return { apiVersion, uiVersion, algorithm };
});
