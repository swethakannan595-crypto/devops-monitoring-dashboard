# 🚀 DevOps Monitoring Dashboard

A real-time infrastructure monitoring platform built with **FastAPI, Prometheus, Grafana, Docker, and Alertmanager**. It provides centralized visibility into system resources, processes, Docker containers, application metrics, and infrastructure alerts through a single monitoring dashboard.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139+-009688?logo=fastapi&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-F46800?logo=grafana&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)
![Alertmanager](https://img.shields.io/badge/Alertmanager-Alerting-E6522C)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**DevOps Monitoring Dashboard** is a full-stack monitoring platform that gives real-time visibility into application and infrastructure health from a single interface.

It collects host-level and container-level metrics, exposes them through a Prometheus-compatible endpoint, visualizes time-series data in Grafana, and sends automated alerts through Alertmanager when configured resource thresholds are exceeded.

The project combines backend development, system monitoring, containerization, observability, alerting, and DevOps practices into one practical monitoring solution.

---

## 🎯 Project Goals

- Monitor real-time system resource utilization
- Track running processes and network activity
- Monitor Docker containers and container resources
- Expose application metrics for Prometheus
- Visualize infrastructure metrics using Grafana
- Detect abnormal resource utilization
- Send automated email notifications through Alertmanager
- Provide REST APIs for monitoring data
- Build a foundation for scalable infrastructure monitoring

---

## ✨ Key Features

### 🖥️ System Monitoring
Real-time host resource monitoring using `psutil`:
- CPU utilization
- Memory utilization
- Disk utilization
- Network traffic
- Running process count
- System information
- Application uptime

### 🐳 Docker Monitoring
Monitor the Docker environment directly from the application, using the **Docker SDK for Python**:
- Docker daemon status
- Total and running container counts
- Container information and statistics
- Docker images
- Per-container resource monitoring

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
application_uptime_seconds
http_requests_total
http_request_duration_seconds
```

Metrics are updated continuously in the background and can be scraped by Prometheus.

### 📈 Grafana Visualization
Grafana visualizes the collected Prometheus metrics through time-series dashboards. Planned panels:
- CPU, memory, and disk usage
- Network traffic
- Running processes
- Docker containers
- Application uptime
- Resource utilization trends

### 🚨 Automated Alerting
Threshold-based infrastructure alerts through Prometheus and Alertmanager:

| Alert             | Condition    | Duration  |
|-------------------|-------------|-----------|
| High CPU Usage    | CPU > 80%    | 2 minutes |
| High Memory Usage | Memory > 85% | 2 minutes |
| High Disk Usage   | Disk > 90%   | 5 minutes |

**Alert flow:**

```text
System Metrics → Prometheus → Alert Rules → Alertmanager → Email Notification
```

Email alerting has been tested successfully with Alertmanager.

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      FastAPI App      │
                         │                       │
                         │  REST APIs            │
                         │  System Monitoring    │
                         │  Docker Monitoring    │
                         │  /metrics             │
                         └──────────┬────────────┘
                                    │
                         Metrics Collection
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Prometheus       │
                         │                       │
                         │  Metric Storage       │
                         │  Query Engine         │
                         │  Alert Evaluation     │
                         └──────────┬────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │                                    │
                  ▼                                    ▼
        ┌──────────────────┐                ┌──────────────────┐
        │      Grafana      │                │   Alertmanager   │
        │                   │                │                  │
        │  Visualization    │                │  Alert Routing   │
        │  Dashboards       │                │  Notifications   │
        └───────────────────┘                └────────┬─────────┘
                                                        │
                                                        ▼
                                                Email Notification
```

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
| Frontend               | HTML5, CSS3, JavaScript  |
| UI Framework           | Bootstrap 5              |
| Templates               | Jinja2                   |
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
│   │   └── index.html
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

| Resource            | URL                                |
|----------------------|-------------------------------------|
| Dashboard            | http://127.0.0.1:8000/dashboard    |
| API                  | http://127.0.0.1:8000              |
| Swagger UI           | http://127.0.0.1:8000/docs         |
| ReDoc                | http://127.0.0.1:8000/redoc        |
| Health Check         | http://127.0.0.1:8000/health       |
| Prometheus Metrics   | http://127.0.0.1:8000/metrics      |

---

## 📡 API Reference

### System Monitoring

| Method | Endpoint          | Description               |
|--------|--------------------|----------------------------|
| GET    | `/api/system`      | Complete system metrics    |
| GET    | `/api/cpu`          | CPU utilization             |
| GET    | `/api/memory`      | Memory utilization          |
| GET    | `/api/disk`         | Disk utilization             |
| GET    | `/api/network`      | Network statistics          |
| GET    | `/api/processes`    | Running processes           |

### Docker Monitoring

| Method | Endpoint              | Description                 |
|--------|-------------------------|------------------------------|
| GET    | `/docker/status`        | Docker daemon status         |
| GET    | `/docker/containers`    | List containers              |
| GET    | `/docker/running`       | Running containers           |
| GET    | `/docker/images`        | Docker images                |
| GET    | `/docker/info`          | Docker system information    |
| GET    | `/docker/stats`         | Container statistics         |

### Application

| Method | Endpoint     | Description               |
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

Prometheus UI: `http://localhost:9090`

The FastAPI application exposes metrics at `http://localhost:8000/metrics`, which Prometheus scrapes and makes available for querying and alert evaluation.

Example PromQL queries:

```promql
system_cpu_usage_percent
system_memory_usage_percent
system_disk_usage_percent
docker_running_containers
```

---

## 🚨 Alertmanager

Start Alertmanager with:

```bash
alertmanager.exe --config.file=alertmanager.yml
```

Alertmanager UI: `http://localhost:9093`

Current alerting configuration monitors:

```text
CPU > 80%
Memory > 85%
Disk > 90%
```

Alerts are routed through Alertmanager and delivered through configured notification channels such as email.

---

## 📈 Grafana

Start Grafana and open `http://localhost:3000`.

Add Prometheus as a data source: `http://localhost:9090`

Recommended dashboard panels:
- CPU, memory, and disk utilization
- Network traffic
- Running processes
- Docker containers
- Application uptime
- System resource trends
- Alert status

---

## 🐳 Docker

The application integrates with Docker through the Docker SDK for Python, providing visibility across:

```text
Docker Engine → Containers → Container Status → Container Statistics → Prometheus Metrics
```

The project also includes Docker configuration for containerized deployment.

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
- [x] Docker monitoring APIs
- [x] Prometheus metric collection and `/metrics` endpoint
- [x] Prometheus alert rules
- [x] Alertmanager integration and email alert testing
- [x] Swagger / ReDoc API documentation

**In Progress**
- [ ] Complete Grafana dashboards
- [ ] Docker Compose monitoring stack
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Centralized log monitoring
- [ ] Dashboard improvements
- [ ] Monitoring performance optimization

**Planned**
- [ ] User authentication and role-based access
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
