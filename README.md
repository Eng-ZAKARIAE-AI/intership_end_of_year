#  RAG-Driven Intelligent IT Maintenance Platform

An enterprise-grade, AI-powered predictive maintenance and technical assistant platform designed to monitor IT infrastructure, detect real-time anomalies, anticipate hardware failures, and assist technicians via Retrieval-Augmented Generation (RAG)[cite: 1].

---

##  Objectives

* **Primary Objective:** Eliminate reliance on manual monitoring and external scraping by enabling direct hardware log ingestion and automated system health tracking[cite: 1].
* **Advanced AI Engineering:** Implement predictive AI models and time-series anomaly detection algorithms to forecast hardware failures (e.g., storage degradation, system log errors, and device performance bottlenecks) and deliver actionable maintenance recommendations before downtime occurs[cite: 1].

---

## Global Architecture

![Global Architecture](assets/11.png)

---

## Repository Structure

```text
rag-it-maintenance/
├── docs/                   # System documentation & UML diagrams
├── services/
│   ├── agent/              # Monitoring Agent (WMI, SNMP, Event Logs)
│   ├── backend/            # FastAPI REST API & Database Connectors
│   ├── frontend/           # React Supervision Dashboard
│   ├── ml-engine/          # Anomaly Detection & Predictive Models
│   └── rag-service/        # RAG Engine, Document Loaders & Vector Store
├── docker-compose.yml      # Multi-container orchestration (PostgreSQL, InfluxDB, ChromaDB)
├── Makefile                # Shortcut CLI commands for development
└── README.md

## 3. Recommended Git Commit Conventions (Best Practice)

When pushing future features throughout your project timeline, enforce **Conventional Commits** for clean team tracking[cite: 1]:

| Prefix | Usage Example |
| :--- | :--- |
| `feat:` | `feat(agent): add WMI parser for SMART disk health` |
| `fix:` | `fix(backend): patch InfluxDB write timeout during CPU spikes` |
| `docs:` | `docs(rag): upload vendor manuals to vector index directory` |
| `ci:` | `ci: add GitHub Actions workflow for pytest and linting` |