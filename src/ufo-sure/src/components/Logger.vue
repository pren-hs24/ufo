<script lang="ts" setup>
import { onMounted, ref, computed, onBeforeUnmount } from "vue";

interface ILog {
    level: "CRITICAL" | "ERROR" | "WARNING" | "INFO" | "DEBUG" | "NOTSET";
    message: string;
    timestamp: Date;
}

const ws = ref<WebSocket | null>(null);
const log = ref<ILog[]>([]);

const host = window.location.host.replace("5173", "8080");
const protocol = window.location.protocol === "https:" ? "wss" : "ws";

const connectWebSocket = () => {
    ws.value = new WebSocket(`${protocol}://${host}/api/monitoring`);
    ws.value.onopen = onWsOpen;
};

const onWsClose = () => {
    console.log("[WebSocket] connection closed");
    setTimeout(connectWebSocket, 1000);
};

function onWsOpen(this: WebSocket) {
    console.log("[WebSocket] connection opened");
    this.onerror = (error: Event) => {
        console.error("[WebSocket] error", error);
    };
    this.onmessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data);
        if (data.type === "log") {
            log.value.push({
                ...data.data,
                timestamp: new Date(data.data.timestamp),
            });
            if (log.value.length > 100) {
                log.value.shift();
            }
        }
    };
    this.onclose = onWsClose;
}

onMounted(() => {
    connectWebSocket();
});

onBeforeUnmount(() => {
    if (!ws.value) return;

    ws.value.onclose = null;
    ws.value.close();
});
</script>
<template>
    <div class="logger">
        <p
            v-for="log in log"
            class="log"
        >
            <span>{{ log.timestamp.toLocaleString() }}</span>
            <span
                class="level"
                :class="log.level"
                >{{ log.level }}</span
            >
            <span>{{ log.message }}</span>
        </p>
    </div>
</template>

<style scoped>
.log {
    display: grid;
    grid-template-columns: 18ch 7ch 1fr;
    gap: 1ch;
    font-size: 1rem;
    margin: 0.25em;

    .level {
        &.INFO {
            color: var(--blue);
        }

        &.WARNING {
            color: var(--yellow);
        }

        &.ERROR,
        &.CRITICAL {
            color: var(--red);
        }
    }
}

.logger {
    display: flex;
    flex-direction: column-reverse;
}
</style>
