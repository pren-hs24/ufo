<script lang="ts" setup>
import { computed, ref, watch } from "vue";
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

/*watch(stepsAndCommands.value, (newStepsAndCommands) => {
    // convert all ICommand to IStep
    steps.value = newStepsAndCommands.map((stepOrCommand) => {
        if ("execute" in stepOrCommand) {
            // This is an ICommand
            return {
                command: stepOrCommand as ICommand,
                parameters: {},
            };
        } else {
            return stepOrCommand as IStep;
        }
    });
});*/

interface IOnChanged {
    added?: { element: ICommand; newIndex: number };
    removed?: { element: IStep; index: number };
    moved?: { element: IStep; oldIndex: number; newIndex: number };
}

const onChanged = ({ added, removed, moved }: IOnChanged) => {
    console.log(
        "onChanged",
        { added, removed, moved },
        stepsAndCommands.value.map((x) => x.name ?? x.command.name),
    );

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
                description: "Speed in km/h",
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
        name: "Wait",
        icon: "fa-solid fa-clock",
        description: "Wait for a specified duration",
        parameters: [
            {
                name: "duration",
                type: "number",
                required: true,
                description: "Duration in seconds",
            },
        ],
        execute: async (params: Record<string, any>) => {
            console.log(`Waiting for ${params.duration} seconds`);
            return new Promise((resolve) => setTimeout(resolve, params.duration * 1000));
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
];

const addStep = (command: ICommand) => {
    steps.value.push({ command, parameters: {} });
};

const removeStep = (index: number) => {
    steps.value.splice(index, 1);
};

const executeSteps = async () => {
    for (const step of steps.value) {
        await step.command.execute(step.parameters);
    }
};
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
                    <h3><i :class="step.command.icon"></i> {{ step.command.name }}</h3>
                    <p class="description">{{ step.command.description }}</p>
                    <button
                        @click="removeStep(index)"
                        class="remove"
                    >
                        <i class="fa-solid fa-trash"></i>
                    </button>
                    <div
                        v-for="(param, paramIndex) in step.command.parameters"
                        :key="paramIndex"
                        :title="param.description"
                        class="parameter"
                    >
                        <label>{{ param.name }} ({{ param.type }})</label>
                        <input
                            v-model="step.parameters[param.name]"
                            :type="param.type"
                            :required="param.required"
                            :min="param.min"
                            :max="param.max"
                        />
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
            @click="executeSteps"
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
    padding: 1em;
    background-color: var(--bg);
    border-radius: 0.5em;
    border: 1px solid var(--border);
    font-family: "Space Grotesk", monospace;
}

#execute {
    grid-column: span 2;
    font-weight: 900;
}

.h-full {
    height: 100%;
}

.step,
.command {
    background-color: var(--bg-mute);
    border-radius: 0.25em;
    padding: 1em;
    border: 1px solid var(--border);
    cursor: move;
    position: relative;
    display: flex;
    flex-direction: column;

    & h3,
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
        color: var(--text-mute);
        font-style: italic;
    }
}

.list {
    display: flex;
    flex-direction: column;
    gap: 1em;
}

.parameter {
    display: flex;
    flex-direction: column;
    margin-top: 1em;

    & label {
        font-weight: bold;
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
