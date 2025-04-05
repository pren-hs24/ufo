<script setup lang="ts">
import { useSystemStore } from "@/stores/system";
import Logger from "@/components/Logger.vue";
import ScriptRunner from "@/components/ScriptRunner.vue";

const systemStore = useSystemStore();
</script>

<template>
    <main>
        <div class="title">
            <h1>UFO-sure</h1>
            {{ systemStore.uiVersion }} | {{ systemStore.apiVersion }}
        </div>
    </main>
    <ScriptRunner />
    <Logger />
</template>

<style scoped>
div.title {
    margin: 1rem;

    & h1 {
        margin-bottom: 0;
    }
}
</style>
