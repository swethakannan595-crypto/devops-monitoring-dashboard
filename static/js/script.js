/*=====================================================
        DEVOPS MONITORING DASHBOARD
        Part 1 - API Integration
======================================================*/

// ===============================
// Base URL
// ===============================

const API_URL = "http://127.0.0.1:8000";


// ===============================
// Fetch API Helper
// ===============================

async function fetchData(endpoint){

    try{

        const response = await fetch(`${API_URL}${endpoint}`);

        if(!response.ok){

            throw new Error("Failed to fetch data");

        }

        return await response.json();

    }

    catch(error){

        console.error(endpoint,error);

        return null;

    }

}


// ===============================
// CPU Usage
// ===============================

async function loadCPU(){

    const data = await fetchData("/cpu");

    if(data){

        document.getElementById("cpu").innerHTML =
            data.cpu_usage + " %";

        const bar = document.getElementById("cpu-bar");

        if(bar){

            bar.style.width = data.cpu_usage + "%";

        }

    }

}


// ===============================
// Memory Usage
// ===============================

async function loadMemory(){

    const data = await fetchData("/memory");

    if(data){

        document.getElementById("memory").innerHTML =
            data.percent + " %";

        const bar = document.getElementById("memory-bar");

        if(bar){

            bar.style.width = data.percent + "%";

        }

    }

}


// ===============================
// Disk Usage
// ===============================

async function loadDisk(){

    const data = await fetchData("/disk");

    if(data){

        document.getElementById("disk").innerHTML =
            data.percent + " %";

        const bar = document.getElementById("disk-bar");

        if(bar){

            bar.style.width = data.percent + "%";

        }

    }

}


// ===============================
// Network Usage
// ===============================

async function loadNetwork(){

    const data = await fetchData("/network");

    if(data){

        document.getElementById("network").innerHTML =

        "↑ " +

        (data.bytes_sent / (1024*1024)).toFixed(2)

        +

        " MB"

        +

        "<br>"

        +

        "↓ "

        +

        (data.bytes_recv / (1024*1024)).toFixed(2)

        +

        " MB";

    }

}


// ===============================
// Load System Monitoring
// ===============================

async function loadSystem(){

    await loadCPU();

    await loadMemory();

    await loadDisk();

    await loadNetwork();

}


// ===============================
// Initial Load
// ===============================

loadSystem();


// ===============================
// Auto Refresh Every 5 Seconds
// ===============================

setInterval(loadSystem,5000);
/*=====================================================
        DEVOPS MONITORING DASHBOARD
        Part 2 - Docker & System Information
======================================================*/

// ===============================
// Docker Running Containers
// ===============================

async function loadDocker(){

    const data = await fetchData("/docker/running");

    const dockerValue = document.getElementById("docker");

    const dockerBar = document.getElementById("docker-bar");

    const tableBody = document.getElementById("docker-table");

    if(!data){

        return;

    }

    if(Array.isArray(data)){

        dockerValue.innerHTML = data.length + " Running";

        if(dockerBar){

            dockerBar.style.width = (data.length * 10) + "%";

        }

        if(tableBody){

            tableBody.innerHTML = "";

            data.forEach(container =>{

                tableBody.innerHTML += `

                <tr>

                    <td>${container.name}</td>

                    <td>${container.id.substring(0,12)}</td>

                    <td>

                        <span class="status-running">

                            Running

                        </span>

                    </td>

                </tr>

                `;

            });

        }

    }

}


// ===============================
// Application Uptime
// ===============================

async function loadUptime(){

    const data = await fetchData("/metrics");

    if(!data){

        return;

    }

    const uptimeElement = document.getElementById("uptime");

    if(uptimeElement){

        const seconds = Math.floor(performance.now()/1000);

        const hours = Math.floor(seconds/3600);

        const minutes = Math.floor((seconds%3600)/60);

        const sec = seconds%60;

        uptimeElement.innerHTML =

            hours +

            "h " +

            minutes +

            "m " +

            sec +

            "s";

    }

}


// ===============================
// Refresh Complete Dashboard
// ===============================

async function refreshDashboard(){

    await loadCPU();

    await loadMemory();

    await loadDisk();

    await loadNetwork();

    await loadDocker();

    await loadUptime();

}


// ===============================
// Auto Refresh
// ===============================

refreshDashboard();

setInterval(refreshDashboard,5000);


// ===============================
// Last Updated Time
// ===============================

function updateTime(){

    const now = new Date();

    const element = document.getElementById("last-update");

    if(element){

        element.innerHTML = now.toLocaleTimeString();

    }

}

updateTime();

setInterval(updateTime,1000);


// ===============================
// Dashboard Loaded
// ===============================

window.addEventListener("load",()=>{

    console.log("DevOps Monitoring Dashboard Loaded");

});
/*=====================================================
        DEVOPS MONITORING DASHBOARD
        Part 3 - Live Charts
======================================================*/

// ===============================
// Arrays for Chart Data
// ===============================

const labels = [];

const cpuData = [];

const memoryData = [];


// ===============================
// CPU Chart
// ===============================

const cpuChart = new Chart(

    document.getElementById("cpuChart"),

    {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "CPU Usage (%)",

                    data: cpuData,

                    borderColor: "#2563eb",

                    backgroundColor: "rgba(37,99,235,0.2)",

                    fill: true,

                    tension: 0.4

                }

            ]

        },

        options: {

            responsive: true,

            animation: true,

            scales: {

                y: {

                    min: 0,

                    max: 100

                }

            }

        }

    }

);


// ===============================
// Memory Chart
// ===============================

const memoryChart = new Chart(

    document.getElementById("memoryChart"),

    {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Memory Usage (%)",

                    data: memoryData,

                    borderColor: "#16a34a",

                    backgroundColor: "rgba(22,163,74,0.2)",

                    fill: true,

                    tension: 0.4

                }

            ]

        },

        options: {

            responsive: true,

            animation: true,

            scales: {

                y: {

                    min: 0,

                    max: 100

                }

            }

        }

    }

);


// ===============================
// Update Charts
// ===============================

async function updateCharts(){

    const cpu = await fetchData("/cpu");

    const memory = await fetchData("/memory");

    const currentTime = new Date().toLocaleTimeString();


    if(labels.length >= 10){

        labels.shift();

        cpuData.shift();

        memoryData.shift();

    }


    labels.push(currentTime);

    cpuData.push(cpu.cpu_usage);

    memoryData.push(memory.percent);


    cpuChart.update();

    memoryChart.update();

}


// ===============================
// Initial Chart Load
// ===============================

updateCharts();


// ===============================
// Refresh Every 5 Seconds
// ===============================

setInterval(updateCharts,5000);


// ===============================
// Resize Charts Automatically
// ===============================

window.addEventListener("resize",()=>{

    cpuChart.resize();

    memoryChart.resize();

});


// ===============================
// Console Message
// ===============================

console.log("Charts Initialized Successfully");
/*=====================================================
        DEVOPS MONITORING DASHBOARD
        Part 4 - UI Features & Initialization
======================================================*/

// ===============================
// Loading Screen
// ===============================

window.addEventListener("load", () => {

    const loader = document.querySelector(".loader");

    if (loader) {

        setTimeout(() => {

            loader.classList.add("hidden");

        }, 1000);

    }

});


// ===============================
// Back To Top Button
// ===============================

const topButton = document.getElementById("topBtn");

window.onscroll = function () {

    if (document.documentElement.scrollTop > 300) {

        if (topButton) {

            topButton.style.display = "block";

        }

    }

    else {

        if (topButton) {

            topButton.style.display = "none";

        }

    }

};

if (topButton) {

    topButton.onclick = function () {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    };

}


// ===============================
// CPU Alert
// ===============================

async function checkCPUAlert() {

    const data = await fetchData("/cpu");

    if (!data) return;

    if (data.cpu_usage >= 80) {

        alert("⚠ High CPU Usage : " + data.cpu_usage + "%");

    }

}


// ===============================
// Memory Alert
// ===============================

async function checkMemoryAlert() {

    const data = await fetchData("/memory");

    if (!data) return;

    if (data.percent >= 80) {

        alert("⚠ High Memory Usage : " + data.percent + "%");

    }

}


// ===============================
// Dashboard Animation
// ===============================

function animateCards() {

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";

        card.style.transform = "translateY(30px)";

        setTimeout(() => {

            card.style.transition = "all .5s ease";

            card.style.opacity = "1";

            card.style.transform = "translateY(0px)";

        }, index * 150);

    });

}


// ===============================
// Update Last Refresh
// ===============================

function updateRefreshTime() {

    const element = document.getElementById("last-update");

    if (element) {

        element.innerHTML = new Date().toLocaleTimeString();

    }

}


// ===============================
// Complete Dashboard Refresh
// ===============================

async function refreshEverything() {

    await loadSystem();

    await loadDocker();

    await updateCharts();

    await checkCPUAlert();

    await checkMemoryAlert();

    updateRefreshTime();

}


// ===============================
// Refresh Every 5 Seconds
// ===============================

setInterval(refreshEverything, 5000);


// ===============================
// Dashboard Startup
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    console.log("===================================");

    console.log(" DevOps Monitoring Dashboard ");

    console.log(" Version : 1.0.0");

    console.log(" Developed by : Swetha Kannan");

    console.log("===================================");

    animateCards();

    refreshEverything();

});


// ===============================
// Keyboard Shortcut
// Press R to Refresh Dashboard
// ===============================

document.addEventListener("keydown", (event) => {

    if (event.key === "r" || event.key === "R") {

        refreshEverything();

    }

});


// ===============================
// Connection Status
// ===============================

window.addEventListener("online", () => {

    console.log("Internet Connected");

});

window.addEventListener("offline", () => {

    console.log("Internet Disconnected");

});


// ===============================
// Dashboard Finished
// ===============================

console.log("Dashboard JavaScript Loaded Successfully");