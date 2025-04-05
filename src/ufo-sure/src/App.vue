<script setup lang="ts">
import { RouterView } from "vue-router";
import Sidebar from "./components/Sidebar.vue";
</script>

<template>
    <div class="body">
        <Sidebar />
        <div class="content">
            <RouterView />
        </div>
    </div>
</template>

<style scoped>
.body {
    position: relative;
    display: flex;
    flex-direction: row;
    gap: 1em;

    .content {
        max-height: calc(100svh - 2em);
        overflow: auto;
        padding: 1em;
        flex: 1;
    }
}
</style>
