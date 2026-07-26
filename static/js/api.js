const API_BASE = "/monitor";

async function getCPU() {
    const response = await fetch(`${API_BASE}/cpu`);
    return await response.json();
}

async function getMemory() {
    const response = await fetch(`${API_BASE}/memory`);
    return await response.json();
}

async function getDisk() {
    const response = await fetch(`${API_BASE}/disk`);
    return await response.json();
}

async function getNetwork() {
    const response = await fetch(`${API_BASE}/network`);
    return await response.json();
}

async function getSystem() {
    const response = await fetch(`${API_BASE}/system`);
    return await response.json();
}

async function getProcesses() {
    const response = await fetch(`${API_BASE}/processes`);
    return await response.json();
}