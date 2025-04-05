<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useSystemStore } from "@/stores/system";

const systemStore = useSystemStore();

const expanded = ref(false);
const KEY = "ufo-sure.sidebar-expanded";

const setSidebarWidth = () => {
    const body = document.querySelector("body");
    if (body) {
        body.style.setProperty("--sidebar-width", expanded.value ? "220px" : "70px");
    }
};

onMounted(() => {
    expanded.value = window.localStorage.getItem(KEY) === "true";
    setSidebarWidth();
});

const toggleExpanded = () => {
    expanded.value = !expanded.value;
    window.localStorage.setItem(KEY, expanded.value.toString());
    setSidebarWidth();
};
</script>

<template>
    <aside :class="{ expanded }">
        <div class="title">
            <h1>{{ expanded ? "UFO" : "U" }}</h1>
        </div>
        <div class="nav">
            <RouterLink
                to="/"
                class="navitem"
            >
                <i class="fa-solid fa-house"></i>
                <span class="label">Home</span>
            </RouterLink>
            <RouterLink
                to="/logger"
                class="navitem"
            >
                <i class="fa-solid fa-chart-simple"></i>
                <span class="label">Logger</span>
            </RouterLink>
            <RouterLink
                to="/script"
                class="navitem"
            >
                <i class="fa-solid fa-code"></i>
                <span class="label">Script Runner</span>
            </RouterLink>
        </div>
        <div class="settings">
            <template v-if="expanded">
                <p class="version">{{ systemStore.uiVersion }}</p>
                <p class="version">{{ systemStore.apiVersion }}</p>
            </template>
            <div
                class="navitem"
                @click="toggleExpanded"
            >
                <template v-if="expanded">
                    <i class="fa-solid fa-chevron-left"></i>
                    <span class="label">Collapse</span>
                </template>
                <template v-else>
                    <i class="fa-solid fa-chevron-right"></i>
                    <span class="label">Expand</span>
                </template>
            </div>
        </div>
    </aside>
</template>

<style scoped>
aside {
    height: calc(100svh - 4em - 2px);
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 0 2em 2em 0;
    padding: 1em;
    margin: 1em 0;
    container-type: inline-size;
    flex-grow: 0;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 35px;

    &.expanded {
        width: calc(var(--sidebar-width) + 2em);

        .label {
            display: inherit;
        }
    }
}

.version {
    margin: 0;
    color: var(--fg-mute);
}

.navitem {
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    gap: 0.5em;
    padding: 0 0.5em;
    border-radius: 0.5em;
    transition: background-color 0.2s;
    color: var(--color-text);
    height: 42px;
    width: 100%;

    &.router-link-active {
        background: var(--bg-mute);
        color: var(--accent);
    }

    &:hover {
        background: var(--bg-mute);
    }

    .label {
        width: 100%;
        display: none;
    }
}

@container (max-width: 150px) {
    .navitem {
        gap: 0;
        padding: 0;
        justify-content: center;
    }

    .label {
        display: none;
    }
}
</style>
