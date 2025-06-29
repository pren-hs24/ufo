<script setup lang="ts">
import api from "@/api";
import { useSystemStore } from "@/stores/system";
import { onMounted, ref } from "vue";

const systemStore = useSystemStore();
const algorithms = ref<string[]>([]);

onMounted(async () => {
    algorithms.value = await api.system.algorithmList();
});

const reset = () => {
    api.system.reset();
};
</script>

<template>
    <div class="title">
        <h2>Settings</h2>
    </div>
    <p>Current algorithm: {{ systemStore.algorithm || "<None>" }}</p>
    <button
        class="primary"
        @click="reset"
    >
        Reset
    </button>
</template>
