# 🚀 DevOps Monitoring Dashboard

A real-time DevOps monitoring platform built with **FastAPI**, **Prometheus**, **Grafana**, and **Docker**. It provides live visibility into system performance, running processes, container health, and application metrics through a modern, responsive web dashboard.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📌 Overview

This project consolidates system, process, container, and application-level metrics into a single dashboard — designed to give developers and DevOps engineers a fast, at-a-glance view of infrastructure health, without needing to jump between multiple tools.

---

## ✨ Features

**System Monitoring**
- CPU, memory, and disk usage
- Network statistics
- System information
- Running process tracking

**Docker Monitoring**
- Container status and health
- Live container list
- Per-container resource usage

**Metrics & Visualization**
- Prometheus metrics endpoint
- Grafana dashboards for time-series visualization
- Real-time updates

**API & Developer Experience**
- FastAPI backend with async support
- Interactive Swagger / ReDoc documentation
- Structured JSON responses and error handling
- Health check endpoint

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, Uvicorn |
| Monitoring | Prometheus, Grafana, psutil |
| Containerization | Docker, Docker SDK for Python |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5, Jinja2 |

---

## 📂 Project Structure

```
devops-monitor-dashboard/
│
├── app/
│   ├── api/
│   │   ├── dashboard.py
│   │   ├── monitoring.py
│   │   ├── process.py
│   │   ├── prometheus.py
│   │   └── docker.py
│   │
│   ├── routers/
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── services/
│   ├── models/
│   └── main.py
│
├── prometheus/
│   └── prometheus.yml
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
└── LICENSE
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.12+
- Docker (optional, for containerized deployment)
- Prometheus & Grafana (for full monitoring stack)

### 1. Clone the repository

```bash
git clone https://github.com/swethakannan595-crypto/devops-monitoring-dashboard.git
cd devops-monitor-dashboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your own values — **never commit your actual `.env` file**.

```bash
cp .env.example .env
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

| Resource | URL |
|---|---|
| Application | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## 📊 Prometheus Setup

```bash
prometheus.exe --config.file=prometheus.yml
```

Access the Prometheus UI at:
```
http://localhost:9090
```

---

## 📈 Grafana Setup

1. Start your Grafana server and open:
   ```
   http://localhost:3000
   ```
2. Log in with the default credentials (change these immediately in production):
   ```
   Username: admin
   Password: admin
   ```
3. Add Prometheus as a data source:
   ```
   URL: http://localhost:9090
   ```
4. Build dashboards using the exposed Prometheus metrics.

---

## 📡 API Reference

### Monitoring

| Method | Endpoint | Description |
|---|---|---|
| GET | `/monitor/cpu` | CPU usage |
| GET | `/monitor/memory` | Memory usage |
| GET | `/monitor/disk` | Disk usage |
| GET | `/monitor/network` | Network statistics |
| GET | `/monitor/system` | System information |
| GET | `/monitor/processes` | Running processes |

### Docker

| Method | Endpoint | Description |
|---|---|---|
| GET | `/docker/status` | Docker daemon status |
| GET | `/docker/containers` | Running containers |
| GET | `/docker/info` | Docker system information |

### Metrics

| Method | Endpoint | Description |
|---|---|---|
| GET | `/metrics` | Prometheus-formatted metrics |

Full interactive documentation is available via Swagger at `/docs`.

---

## 🗺️ Roadmap

- [ ] Email and Slack alerting
- [ ] Kubernetes monitoring support
- [ ] Centralized log monitoring
- [ ] User authentication & role-based access control
- [ ] Historical metrics storage
- [ ] AI-based anomaly detection
- [ ] Multi-server monitoring
- [ ] Dark mode dashboard

---

## 🤝 Contributing

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes
   ```bash
   git commit -m "Add: new feature description"
   ```
4. Push to your branch
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Swetha Kannan**
Final Year B.Sc. Information Technology | Python & FastAPI Developer | DevOps Enthusiast

---

## ⭐ Support

If this project helped you, consider giving it a star on GitHub — it helps others discover it too.
