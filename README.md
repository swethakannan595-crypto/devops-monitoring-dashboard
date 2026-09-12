<div align="center">

# 🚀 DevOps Monitoring Dashboard

A real-time infrastructure monitoring platform built with **FastAPI, Prometheus, Grafana, Docker, and Alertmanager** — with a multi-page dashboard for system, process, service, and container observability.

🔗 Live Demo: https://devops-monitoring-dashboard-zrgq.onrender.com/dashboard

</div>

---

## 📌 Overview

**DevOps Monitoring Dashboard** is a full-stack monitoring platform that gives real-time visibility into application and infrastructure health from a single interface.

It collects host-level and container-level metrics, exposes them through a Prometheus-compatible endpoint, visualizes time-series data in Grafana, and sends automated alerts through Alertmanager when configured resource thresholds are exceeded. The dashboard itself is a multi-page single-file frontend — System Monitor, Docker, Processes, Services, Logs, and Alerts each live on their own view with live search, filtering, and auto-refresh.

The project combines backend development, system monitoring, containerization, observability, alerting, CI/CD, and DevOps practices into one practical monitoring solution.


  <img width="946" height="436" alt="image" src="https://github.com/user-attachments/assets/ee48cf6f-9c7f-4ab8-ae0b-65cfb0032af4" />


---

## 🎯 Project Goals

- Monitor real-time system resource utilization
- Track running processes and network activity
- Monitor Docker containers, images, and per-container resource usage
- Track Windows services and their running/stopped state
- Expose application metrics for Prometheus
- Visualize infrastructure metrics using Grafana
- Detect abnormal resource utilization and surface alert status
- Send automated email notifications through Alertmanager
- Provide REST APIs for monitoring data
- Automate build and deployment with GitHub Actions and Docker Hub
- Build a foundation for scalable infrastructure monitoring

---

## ✨ Key Features

### 🖥️ System Monitoring
Real-time host resource monitoring using `psutil`:
- CPU utilization, physical/logical core count, frequency
- Memory utilization (total, used, available)
- Disk utilization (total, used, free)
- Network traffic (bytes and packets sent/received)
- Running process count
- System information (hostname, OS, architecture, processor)
- Application uptime

    <img width="957" height="431" alt="image" src="https://github.com/user-attachments/assets/0079c02d-61b8-4209-944a-47862e258edb" />



### 🐳 Docker Monitoring
A dedicated Docker view with tabs for **Containers**, **Images**, **Live Stats**, and **Info**, built on the **Docker SDK for Python**:
- Docker daemon status
- Running vs. total container counts, with per-container status
- Docker image list with tags and size
- Live per-container CPU/memory stats
- Docker system information (version, OS, architecture)

   <img width="954" height="431" alt="image" src="https://github.com/user-attachments/assets/467f54e6-a6ff-4125-bd26-b484629db113" />
   


### 📋 Process Monitoring
A searchable process monitor page:
- Full process list with PID, name, CPU %, memory %, and status
- Top CPU and Top Memory quick filters
- Live search by process name
- Auto-refreshing table

   <img width="946" height="436" alt="image" src="https://github.com/user-attachments/assets/ba9f0c3a-2854-4b87-a985-07c0f25883f6" />
   



### ⚙️ Windows Service Monitoring
A dedicated services page:
- Full service list with name, display name, status, and start type
- Filter by Running / Stopped / All
- Live search by service name

  <img width="947" height="435" alt="image" src="https://github.com/user-attachments/assets/6a78a215-1ac0-43ad-b4e3-e7f51cac07a0" />
  


### 📊 Prometheus Metrics
The application exposes monitoring data at:

```text
GET /metrics
```

Currently available Prometheus-compatible metrics:

```text
system_cpu_usage_percent
system_memory_usage_percent
system_disk_usage_percent
system_network_bytes_sent
system_network_bytes_received
system_running_processes
docker_running_containers
docker_total_containers
docker_container_cpu_percent{container="..."}
docker_container_memory_percent{container="..."}
application_uptime_seconds
http_requests_total
http_request_duration_seconds
```

 <img width="952" height="436" alt="image" src="https://github.com/user-attachments/assets/57763e67-39a3-4366-b554-a6c4907adae3" />

  


The dashboard's Prometheus view parses this endpoint client-side to preview key metrics without leaving the app, alongside a link to the raw `/metrics` output.



### 📈 Grafana Visualization
Grafana visualizes the collected Prometheus metrics through time-series dashboards. Panels in progress:
- CPU, memory, and disk usage
- Network traffic
- Running processes and Docker containers
- Docker per-container CPU/memory
- Application uptime and resource trends

  <img width="957" height="435" alt="image" src="https://github.com/user-attachments/assets/b5c72bff-4571-41e3-973d-689241c1c268" />


### 🚨 Automated Alerting
Threshold-based infrastructure alerts through Prometheus and Alertmanager, surfaced on a dedicated Alerts page in the dashboard:

| Alert             | Condition    | Duration  |
|-------------------|-------------|-----------|
| High CPU Usage    | CPU > 80%    | 2 minutes |
| High Memory Usage | Memory > 85% | 2 minutes |
| High Disk Usage   | Disk > 90%   | 5 minutes |

The Alerts page shows live rule status (Normal / Warning / High) computed from real metrics, plus an active-alerts feed intended to read from Alertmanager's API.

**Alert flow:**

```text
System Metrics → Prometheus → Alert Rules → Alertmanager → Email Notification
```

Email alerting has been tested successfully with Alertmanager.

  <img width="921" height="433" alt="image" src="https://github.com/user-attachments/assets/e1aeaafc-21f3-4f06-ae1c-30b9fbe3a985" />




### 📄 Log Viewer *(UI in place, backend in progress)*
A log viewer page with:
- Application vs. Docker log source tabs
- Info / Warning / Error severity filters
- Live search across log messages
- Color-coded entries by severity

  <img width="959" height="307" alt="image" src="https://github.com/user-attachments/assets/e5131bda-a5c5-43fb-80ed-69b3b3092334" />
  


### 🔐 Authentication *(UI in place, backend in progress)*
Sign-in and account creation screens are built into the dashboard, ready to connect to session/JWT-based route protection:
- Sign In and Create Account forms
- Account state reflected in the top navigation bar

### 🎨 Dashboard UI
- Multi-page layout (Overview, System Monitor, Prometheus, Docker, Processes, Services, Logs, Alerts) with client-side routing — no full page reloads
- Custom branding and icon set (Font Awesome) throughout
- Auto-refreshing panels with a manual "Refresh All" control
- Responsive layout for smaller screens
- Built entirely on top of a documented REST API (testable via `/docs`)

---

## 🛠️ Technology Stack

| Layer                 | Technology               |
|------------------------|--------------------------|
| Programming Language   | Python 3.12+             |
| Backend Framework      | FastAPI                  |
| ASGI Server            | Uvicorn                  |
| System Monitoring      | psutil                   |
| Metrics                | Prometheus Client        |
| Metrics Collection     | Prometheus               |
| Visualization          | Grafana                  |
| Alerting               | Alertmanager             |
| Containerization       | Docker                   |
| Docker Integration     | Docker SDK for Python    |
| CI                     | GitHub Actions           |
| CD                     | GitHub Actions → Docker Hub |
| Frontend               | HTML5, CSS3, Vanilla JavaScript |
| Icons                  | Font Awesome 6           |
| Templates              | Jinja2                   |
| API Documentation      | Swagger UI / ReDoc       |
| Version Control        | Git & GitHub             |

---

## 📂 Project Structure

```text
devops-monitoring-dashboard/
│
├── app/
│   ├── api/
│   │   ├── monitoring.py
│   │   ├── docker.py
│   │   ├── dashboard.py
│   │   ├── process.py
│   │   └── prometheus.py
│   │
│   ├── monitoring/
│   │   ├── system_monitor.py
│   │   └── prometheus_metrics.py
│   │
│   ├── routers/
│   ├── services/
│   ├── models/
│   │
│   ├── templates/
│   │   └── index.html          # Multi-view dashboard (System, Docker, Processes,
│   │                            # Services, Prometheus, Logs, Alerts, Auth)
│   │
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │
│   └── main.py
│
├── prometheus/
│   ├── prometheus.yml
│   └── alerts.yml
│
├── alertmanager/
│   └── alertmanager.yml
│
├── .github/
│   └── workflows/               # CI (test/build) and CD (Docker Hub push)
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
└── LICENSE
```

> The exact structure may evolve as additional monitoring and DevOps modules are added.

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.12+
- Git
- Docker Desktop
- Prometheus
- Grafana
- Alertmanager

### 1. Clone the repository

```bash
git clone https://github.com/swethakannan595-crypto/devops-monitoring-dashboard.git
cd devops-monitoring-dashboard
```

### 2. Create a virtual environment

**Windows**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

Never commit sensitive credentials such as API keys, SMTP passwords, Gmail app passwords, database credentials, or access tokens.

---

## ▶️ Running the Application

```bash
uvicorn app.main:app --reload
```

 <img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/af80deb2-589b-4da1-99bd-0a3bb7eb77e3" />


---

## 📡 API Reference

### System Monitoring

| Method | Endpoint          | Description                 |
|--------|--------------------|----------------------------|
| GET    | `/api/system`      | Complete system metrics    |
| GET    | `/api/cpu`          | CPU utilization           |
| GET    | `/api/memory`      | Memory utilization         |
| GET    | `/api/disk`         | Disk utilization          |
| GET    | `/api/network`      | Network statistics        |
| GET    | `/api/processes`    | Running processes         |

### Process Monitoring

| Method | Endpoint                    | Description                   |
|--------|-----------------------------|-------------------------------|
| GET    | `/processes/`               | List all running processes    |
| GET    | `/processes/search?name=`   | Search processes by name      |
| GET    | `/processes/top/cpu`        | Top processes by CPU usage    |
| GET    | `/processes/top/memory`     | Top processes by memory usage |

### Windows Service Monitoring

| Method | Endpoint                    | Description                   |
|--------|-----------------------------|-------------------------------|
| GET    | `/services/`                | List all services             |
| GET    | `/services/search?name=`    | Search services by name       |
| GET    | `/services/running`         | List running services         |
| GET    | `/services/stopped`         | List stopped services         |

### Docker Monitoring

| Method | Endpoint                | Description                  |
|--------|-------------------------|------------------------------|
| GET    | `/docker/status`        | Docker daemon status         |
| GET    | `/docker/containers`    | List containers              |
| GET    | `/docker/running`       | Running containers           |
| GET    | `/docker/images`        | Docker images                |
| GET    | `/docker/info`          | Docker system information    |
| GET    | `/docker/stats`         | Live container statistics    |

### Application

| Method | Endpoint      | Description               |
|--------|---------------|----------------------------|
| GET    | `/api/info`   | Application information    |
| GET    | `/health`     | Application health check   |
| GET    | `/metrics`    | Prometheus metrics         |

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

---

## 📊 Prometheus Configuration

Start Prometheus with the project configuration:

```bash
prometheus.exe --config.file=prometheus.yml

```

  <img width="947" height="435" alt="image" src="https://github.com/user-attachments/assets/957e0949-bd5e-4f3b-88e6-b113ad478499" />
  


Prometheus UI: `http://localhost:9090`

The FastAPI application exposes metrics at `http://localhost:8000/metrics`, which Prometheus scrapes and makes available for querying and alert evaluation.

Example PromQL queries:

```promql
system_cpu_usage_percent
system_memory_usage_percent
system_disk_usage_percent
docker_running_containers
docker_container_cpu_percent{container="devops-dashboard"}
docker_container_memory_percent{container="devops-dashboard"}

```

---

## 🚨 Alertmanager

Start Alertmanager with:

```bash
alertmanager.exe --config.file=alertmanager.yml

```

  <img width="960" height="412" alt="image" src="https://github.com/user-attachments/assets/e4896202-7bb9-49ac-b5ef-f1b847be0226" />
  


Alertmanager UI: `http://localhost:9093`

Current alerting configuration monitors:

```text
CPU > 80%
Memory > 85%
Disk > 90%

```

Alerts are routed through Alertmanager and delivered through configured notification channels such as email. The dashboard's Alerts page is built to read a live alert feed from Alertmanager's API — wiring this up server-side will make it fully live.


---

## 📈 Grafana

Start Grafana and open `http://localhost:3000`.

Add Prometheus as a data source: `http://localhost:9090`

Recommended dashboard panels:
- CPU, memory, and disk utilization
- Network traffic
- Running processes
- Docker containers and per-container resource usage
- Application uptime
- System resource trends
- Alert status


    <img width="866" height="307" alt="image" src="https://github.com/user-attachments/assets/cea84870-3571-464f-909b-c4d332965066" />
    


---

## 🐳 Docker

The application integrates with Docker through the Docker SDK for Python, providing visibility across:


   <img width="957" height="502" alt="image" src="https://github.com/user-attachments/assets/1c0cacdc-a611-4406-99a0-04f19e37125d" />
   
   

```text
Docker Engine → Containers → Container Status → Container Statistics → Prometheus Metrics
```

The dashboard's Docker page surfaces containers, images, live per-container stats, and daemon info in one place. The project also includes Docker configuration for containerized deployment.

---

## 🔁 CI/CD

The project uses **GitHub Actions** for continuous integration and delivery:


<img width="946" height="436" alt="image" src="https://github.com/user-attachments/assets/ade53706-c5c7-4427-8c0b-60e6f8186f38" />



```text
GitHub → GitHub Actions (CI) → Docker Build → Docker Hub (CD)
```

- **CI workflow** runs on every push to `main` — installs dependencies and validates the build.
- **CD workflow** builds the Docker image and pushes it to Docker Hub on successful CI runs.

Workflow runs and history are visible under the repository's **Actions** tab.

---

## 🔍 Monitoring Workflow

```text
1. psutil / Docker SDK
2. FastAPI monitoring layer
3. Prometheus Client Metrics
4. /metrics endpoint
5. Prometheus scraping
6. Grafana visualization
7. Prometheus alert rules
8. Alertmanager
9. Email notification
```

---

## 🧪 Testing the Metrics Endpoint

After starting FastAPI, verify the endpoint:

```powershell
Invoke-WebRequest http://localhost:8000/metrics -UseBasicParsing |
    Select-Object -ExpandProperty Content
```

To check specific metrics:

```powershell
Invoke-WebRequest http://localhost:8000/metrics -UseBasicParsing |
    Select-Object -ExpandProperty Content |
    Select-String "system_cpu_usage_percent|system_memory_usage_percent|system_disk_usage_percent"
```

---

## 🗺️ Roadmap

**Completed**
- [x] FastAPI backend
- [x] System resource monitoring (CPU, memory, disk, network, processes)
- [x] Docker monitoring APIs (status, containers, images, info, stats)
- [x] Prometheus metric collection and `/metrics` endpoint, including per-container Docker metrics
- [x] Prometheus alert rules
- [x] Alertmanager integration and email alert testing
- [x] Swagger / ReDoc API documentation
- [x] Process monitoring API and dashboard page
- [x] Windows service monitoring API and dashboard page
- [x] Multi-page dashboard UI with client-side routing (Overview, System, Docker, Processes, Services, Prometheus, Logs, Alerts)
- [x] GitHub Actions CI/CD pipeline (build → Docker Hub push)

**In Progress**
- [ ] Complete Grafana dashboards
- [ ] Docker Compose monitoring stack
- [ ] Centralized log monitoring (dashboard UI built, backend log feed pending)
- [ ] Live Alertmanager feed on the Alerts page (UI built, backend proxy pending)
- [ ] User authentication and route protection (sign-in/sign-up UI built, backend session/JWT pending)
- [ ] Jenkins pipeline as an alternate/parallel CD path
- [ ] Monitoring performance optimization

**Planned**
- [ ] Role-based access control
- [ ] Kubernetes monitoring
- [ ] Multi-server monitoring
- [ ] Historical analytics
- [ ] AI-based anomaly detection
- [ ] Slack notifications
- [ ] Advanced log analysis
- [ ] Production deployment
- [ ] Dark mode
- [ ] Automated testing and coverage

---

## 🔐 Security

Never commit `.env` files, API keys, passwords, SMTP credentials, Gmail app passwords, or access tokens. Use environment variables and GitHub Secrets for sensitive configuration.

---

## 🤝 Contributing

Contributions and suggestions are welcome.

```bash
git checkout -b feature-name
# make your changes
git add .
git commit -m "Add: feature description"
git push origin feature-name
```

Then open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Swetha Kannan**
Final-Year B.Sc. Information Technology Student
Python & FastAPI Developer | DevOps Enthusiast

Interested in: Backend Development, Python, FastAPI, DevOps, Cloud & Infrastructure, Monitoring & Observability, AI/ML

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub. Feedback, suggestions, and contributions are always welcome.

---

## 📌 Project Status

**Active Development** — this project is continuously evolving as new monitoring capabilities, visualization features, automation, and DevOps practices are added.
