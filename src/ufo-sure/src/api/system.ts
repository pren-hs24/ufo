export const system = {
    version: async () => {
        const res = await fetch("/api/version");
        if (!res.ok) {
            throw new Error("Failed to fetch version");
        }
        const data = await res.text();
        return data;
    },
    reset: async () => {
        const res = await fetch("/api/system/algorithm/reset", { method: "POST" });
        if (!res.ok) {
            throw new Error("Failed to reset");
        }
        const data = await res.text();
        return data;
    },
    algorithm: async () => {
        const res = await fetch("/api/system/algorithm");
        if (!res.ok) {
            throw new Error("Failed to fetch algorithm");
        }
        const data = await res.text();
        return data;
    },
    algorithmList: async () => {
        const res = await fetch("/api/system/algorithms");
        if (!res.ok) {
            throw new Error("Failed to fetch algorithm list");
        }
        const data = await res.json();
        return data;
    },
    setAlgorithm: async (algorithm: string | null) => {
        const res = await fetch("/api/system/algorithm?name=" + algorithm, {
            method: "PUT",
        });
        if (!res.ok) {
            throw new Error("Failed to set algorithm");
        }
        const data = await res.json();
        return data;
    },
};
