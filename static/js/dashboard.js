// ======================================
// DevOps Monitoring Dashboard
// dashboard.js
// ======================================

// API Base URL
const API_BASE = "/monitor";

// Fetch CPU Usage
async function loadCPU() {
    try {
        const response = await fetch(`${API_BASE}/cpu`);
        const data = await response.json();

        document.getElementById("cpu-usage").innerText =
            data.cpu_usage + "%";

    } catch (error) {
        console.error("CPU Error:", error);
    }
}

// Fetch Memory Usage
async function loadMemory() {
    try {
        const response = await fetch(`${API_BASE}/memory`);
        const data = await response.json();

        document.getElementById("memory-usage").innerText =
            data.percent + "%";

    } catch (error) {
        console.error("Memory Error:", error);
    }
}

// Fetch Disk Usage
async function loadDisk() {
    try {
        const response = await fetch(`${API_BASE}/disk`);
        const data = await response.json();

        document.getElementById("disk-usage").innerText =
            data.percent + "%";

    } catch (error) {
        console.error("Disk Error:", error);
    }
}

// Fetch Network Usage
async function loadNetwork() {
    try {
        const response = await fetch(`${API_BASE}/network`);
        const data = await response.json();

        document.getElementById("network-sent").innerText =
            formatBytes(data.bytes_sent);

        document.getElementById("network-received").innerText =
            formatBytes(data.bytes_received);

    } catch (error) {
        console.error("Network Error:", error);
    }
}

// Fetch System Information
async function loadSystem() {
    try {
        const response = await fetch(`${API_BASE}/system`);
        const data = await response.json();

        document.getElementById("hostname").innerText =
            data.hostname;

        document.getElementById("os").innerText =
            data.operating_system;

        document.getElementById("processor").innerText =
            data.processor;

    } catch (error) {
        console.error("System Error:", error);
    }
}

// Format Bytes
function formatBytes(bytes) {

    if (bytes === 0) return "0 B";

    const sizes = ["B", "KB", "MB", "GB", "TB"];

    const i = Math.floor(Math.log(bytes) / Math.log(1024));

    return (
        (bytes / Math.pow(1024, i)).toFixed(2) +
        " " +
        sizes[i]
    );
}

// Load All Data
function loadDashboard() {
    loadCPU();
    loadMemory();
    loadDisk();
    loadNetwork();
    loadSystem();
}

// Initial Load
loadDashboard();

// Auto Refresh Every 2 Seconds
setInterval(loadDashboard, 2000);