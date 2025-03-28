<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useSystemStore } from "@/stores/system";

const systemStore = useSystemStore();
</script>

<template>
    <main>
        <div class="title">
            <h1>UFO-sure</h1>
            {{ systemStore.uiVersion }} | {{ systemStore.apiVersion }}
        </div>
    </main>
</template>

<style scoped>
div.title {
    margin: 1rem;

    & h1 {
        margin-bottom: 0;
    }
}
</style>
