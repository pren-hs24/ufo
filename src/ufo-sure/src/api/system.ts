export const system = {
    version: async () => {
        const res = await fetch("/api/version");
        if (!res.ok) {
            throw new Error("Failed to fetch version");
        }
        const data = await res.text();
        return data;
    },
};
