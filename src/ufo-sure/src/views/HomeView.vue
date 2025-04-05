<script setup lang="ts">
import { useSystemStore } from "@/stores/system";

const systemStore = useSystemStore();
</script>

<template>
    <main>
        <div class="title">
            <h2>Welcome to</h2>
            <h1>UFO</h1>
            {{ systemStore.uiVersion }} | {{ systemStore.apiVersion }}
        </div>
        <div class="quicklinks">
            <RouterLink to="/logger">
                <div class="card">
                    <div class="flow">
                        <i class="icon fa-solid fa-chart-simple"></i>
                        <h3 class="title">Logger</h3>
                        <span class="description"> Monitor device events </span>
                        <div class="align-right">
                            <i class="fa-solid fa-arrow-right"></i>
                        </div>
                    </div>
                </div>
            </RouterLink>
            <RouterLink to="/script">
                <div class="card">
                    <div class="flow">
                        <i class="icon fa-solid fa-code"></i>
                        <h3 class="title">Script Runner</h3>
                        <span class="description">
                            Execute simple commands or configure and run full scripts
                        </span>
                        <div class="align-right">
                            <i class="fa-solid fa-arrow-right"></i>
                        </div>
                    </div>
                </div>
            </RouterLink>
        </div>
    </main>
</template>

<style scoped>
main {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
}

div.title {
    margin: 1rem;

    & h1 {
        margin: 0;
        font-size: 7rem;
    }

    & h2 {
        margin: 0;
    }
}

a .card {
    color: var(--fg);
    padding: 2em;
    height: calc(100% - 4em);

    .flow {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
    }

    .description {
        font-weight: 300;
    }

    & i.icon {
        font-size: 2.5rem;
    }

    & .align-right {
        margin-top: auto;
    }
}

.align-right {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: end;
}

.quicklinks {
    display: grid;
    width: 100%;
    grid-template-columns: repeat(2, 1fr);
    align-items: stretch;
    gap: 1em;
}
</style>
