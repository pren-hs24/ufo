<script lang="ts" setup>
import { ref } from "vue";
import { VueDraggableNext as draggable } from "vue-draggable-next";

type CommandExecution = (params: Record<string, any>) => Promise<void>;

interface ICommand {
    name: string;
    icon: string;
    description: string;
    parameters: Array<{
        name: string;
        type: string;
        required: boolean;
        description: string;
        min?: number;
        max?: number;
        options?: Array<{ label: string; value: any }>;
    }>;
    execute: CommandExecution;
}

interface IStep {
    command: ICommand;
    parameters: Record<string, any>;
}

const stepsAndCommands = ref<(IStep | ICommand)[]>([]);
const steps = ref<IStep[]>([]);
const running = ref(false);

interface IOnChanged {
    added?: { element: ICommand; newIndex: number };
    removed?: { element: IStep; index: number };
    moved?: { element: IStep; oldIndex: number; newIndex: number };
}

const onChanged = ({ added, removed, moved }: IOnChanged) => {
    if (added) {
        const command = added.element;
        steps.value.splice(added.newIndex, 0, {
            command,
            parameters: {},
        });
    } else if (removed) {
        removeStep(removed.index);
    } else if (moved) {
        const items = steps.value.splice(moved.oldIndex, 1);
        steps.value.splice(moved.newIndex, 0, ...items);
    }

    stepsAndCommands.value = [...steps.value];
};

const commands: ICommand[] = [
    {
        name: "Set Speed",
        icon: "fa-solid fa-tachometer-alt",
        description: "Set the speed of the UFO",
        parameters: [
            {
                name: "speed",
                type: "number",
                required: true,
                description: "Speed in %",
                min: -100,
                max: 100,
            },
        ],
        execute: async (params: Record<string, any>) => {
            console.log(`Setting speed to ${params.speed} km/h`);
            await fetch("/api/command/speed", {
                method: "POST",
                body: JSON.stringify({ speed: params.speed }),
            });
        },
    },
    {
        name: "Debug Logging",
        icon: "fa-solid fa-bug",
        description: "Enable or disable debug logging",
        parameters: [
            {
                name: "enable",
                type: "boolean",
                required: true,
                description: "Enable debug logging",
            },
        ],
        execute: async (params: Record<string, any>) => {
            console.log(`Debug logging is now ${params.enable ? "enabled" : "disabled"}`);
            await fetch("/api/command/logging", {
                method: "POST",
                body: JSON.stringify({ enable: params.enable }),
            });
        },
    },
    {
        name: "Destination Reached",
        icon: "fa-solid fa-map-marker-alt",
        description: "Signal that the destination has been reached",
        parameters: [],
        execute: async () => {
            console.log("Destination reached");
            await fetch("/api/command/destination-reached", {
                method: "POST",
            });
        },
    },
    {
        name: "Follow Line",
        icon: "fa-solid fa-road",
        description: "Follow the line until the next point is reached",
        parameters: [],
        execute: async () => {
            console.log("Following line");
            await fetch("/api/command/follow", {
                method: "POST",
            });
        },
    },
    {
        name: "Turn",
        icon: "fa-solid fa-sync-alt",
        description: "Turn the UFO to a specified angle",
        parameters: [
            {
                name: "angle",
                type: "number",
                required: true,
                description: "Angle in degrees",
                min: -180,
                max: 180,
            },
            {
                name: "snap",
                type: "boolean",
                required: false,
                description: "Snap to the nearest line",
            },
        ],
        execute: async (params: Record<string, any>) => {
            console.log(`Turning to ${params.angle} degrees`);
            await fetch("/api/command/turn", {
                method: "POST",
                body: JSON.stringify({ angle: params.angle, snap: params.snap }),
            });
        },
    },
    {
        name: "Wait",
        icon: "fa-solid fa-clock",
        description: "Wait for a specified duration",
        parameters: [
            {
                name: "duration",
                type: "number",
                required: true,
                description: "Duration in milliseconds",
            },
        ],
        execute: async (params: Record<string, any>) => {
            console.log(`Waiting for ${params.duration} seconds`);
            return new Promise((resolve) => setTimeout(resolve, params.duration));
        },
    },
];

const removeStep = (index: number) => {
    steps.value.splice(index, 1);
};

const runScript = async () => {
    if (running.value) return;

    running.value = true;
    for (const step of steps.value) {
        await step.command.execute(step.parameters);
    }
    running.value = false;
};

const paramId = ({ name }: { name: string }) => `param-${name}`;
</script>
<template>
    <div class="editor">
        <div class="steps h-full">
            <h2><i class="fa-solid fa-list"></i> Script Steps</h2>
            <draggable
                class="h-full list"
                :list="stepsAndCommands"
                group="steps"
                @change="onChanged"
            >
                <div
                    v-for="(step, index) in steps"
                    :key="index"
                    class="step"
                >
                    <div class="heading">
                        <h3><i :class="step.command.icon"></i> {{ step.command.name }}</h3>
                        <p class="description">{{ step.command.description }}</p>
                        <button
                            @click="removeStep(index)"
                            class="remove"
                        >
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                    <h4 v-if="step.command.parameters.length">Parameters</h4>
                    <div class="parameters">
                        <div
                            v-for="(param, paramIndex) in step.command.parameters"
                            :key="paramIndex"
                            :title="param.description"
                            class="parameter"
                            :class="'type-' + param.type"
                        >
                            <div class="label-and-description">
                                <label :for="paramId(param)"
                                    >{{ param.name }} ({{ param.type }})</label
                                >
                                <span class="description">{{ param.description }}</span>
                            </div>
                            <input
                                v-if="param.type == 'boolean'"
                                type="checkbox"
                                :id="paramId(param)"
                                :checked="step.parameters[param.name]"
                            />
                            <input
                                v-else
                                v-model="step.parameters[param.name]"
                                :type="param.type"
                                :required="param.required"
                                :min="param.min"
                                :max="param.max"
                                :id="paramId(param)"
                            />
                        </div>
                    </div>
                </div>
            </draggable>
        </div>

        <div class="command-list">
            <h2><i class="fa-solid fa-terminal"></i> Available Commands</h2>
            <draggable
                class="h-full list"
                :list="commands"
                :group="{
                    name: 'steps',
                    pull: 'clone',
                }"
            >
                <div
                    v-for="(command, index) in commands"
                    :key="index"
                    class="command"
                >
                    <h3><i :class="command.icon"></i> {{ command.name }}</h3>
                    <p class="description">{{ command.description }}</p>
                </div>
            </draggable>
        </div>

        <button
            id="execute"
            class="primary"
            :disabled="running"
            @click="runScript"
        >
            Execute Steps
        </button>
    </div>
</template>

<style scoped>
.editor {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1em;
    font-family: "Space Grotesk", monospace;
}

.label-and-description {
    width: 100%;
    display: flex;
    overflow: clip;
    flex-direction: row;
    gap: 0.5em;
    align-items: first baseline;

    &.description {
        color: var(--fg-mute);
    }
}

#execute {
    grid-column: span 2;
    font-weight: 900;

    &:disabled {
        cursor: progress;
    }
}

.h-full {
    height: 100%;
}

h4 {
    text-transform: uppercase;
    letter-spacing: 0.1ch;
    font-size: 0.8rem;
}

.step .heading {
    margin-bottom: 1em;
}

.step,
.command {
    background-color: var(--bg);
    border-radius: 0.25em;
    padding: 1em;
    border: 1px solid var(--border);
    cursor: move;
    position: relative;
    display: flex;
    flex-direction: column;

    & h3,
    h4,
    p {
        margin: 0;
    }

    .remove {
        position: absolute;
        top: 0.5em;
        right: 0.5em;
        background-color: var(--bg-mute);
        border: none;
        cursor: pointer;
        width: max-content;
        padding: 0.5em;

        &:hover {
            color: var(--red);
        }
    }

    .description {
        font-size: 0.8em;
        color: var(--fg-mute);
        font-style: italic;
    }
}

.list {
    display: flex;
    flex-direction: column;
    gap: 1em;
}

.parameters {
    display: flex;
    flex-direction: column;
    gap: 1em;
}

.parameter {
    display: flex;
    flex-direction: column;

    &.type-boolean {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 0.5em;

        & label {
            margin-bottom: 0;
        }
    }

    & label {
        margin-bottom: 0.5em;
    }

    input {
        padding: 0.5em;
        border-radius: 0.25em;
        border: 1px solid var(--border);
        background-color: var(--bg-mute);
        color: var(--text);
    }
}
</style>
