# 🛡️ Cowrie SSH/Telnet Honeypot & Threat Intelligence Dashboard

A full-stack cybersecurity threat intelligence platform that captures, ingests, analyzes, and visualizes real-world SSH and Telnet attack traffic targeting cloud infrastructure.

---

## 📐 System Architecture

```text
       [ Public Internet ]
               │
               ▼ (Port 22 / 2223)
┌──────────────────────────────────────────┐
│  Oracle Cloud VPS (Ubuntu 24.04)         │
│  └─► Cowrie Honeypot (Docker Container)  │
└──────────────────┬───────────────────────┘
                   │  Raw JSON Logs (cowrie.json)
                   ▼  Automated SCP Transfer
┌──────────────────────────────────────────┐
│  Automated ETL Pipeline (pipeline.py)    │
│  └─► Cleans, parses & structures events  │
└──────────────────┬───────────────────────┘
                   │  SQL Insertion
                   ▼
┌──────────────────────────────────────────┐
│  MySQL Database (honeypot_db)            │
│  ├─► login_attempts                      │
│  └─► command_logs                        │
└──────────────────┬───────────────────────┘
                   │  Query & Analytics
                   ▼
┌──────────────────────────────────────────┐
│  Flask Threat Intelligence Dashboard     │
│  └─► Web UI & Matplotlib Analytics       │
└──────────────────────────────────────────┘
```

---

## 🗂️ Project Directory Structure

Visitors can inspect the core Python analysis code, database schemas, and configuration templates below:

```text
cowrie-honeypot-threat-intelligence/
├── analysis/
│   ├── app.py           # Flask web application serving the Threat Intel Dashboard
│   ├── pipeline.py      # Automated background ETL service syncing VPS logs to MySQL
│   ├── analyze_logs.py  # Data aggregation, SQL queries & Matplotlib visualization logic
│   ├── config.py        # Centralized environment & database configuration module
│   └── templates/
│       └── index.html   # Web Dashboard UI template displaying attack analytics
├── data/                # Local log storage directory (ignored by git)
├── docs/                # Project documentation and architecture notes
├── screenshots/         # Screenshots of dashboard and honeypot setup
├── .env.example         # Template for environment configuration
├── .gitignore           # Git ignore file protecting credentials and raw logs
├── docker-compose.yml   # Docker Compose definition for running Cowrie
├── honeypot_db.sql      # MySQL schema initialization dump
└── README.md            # Project documentation
```

---

## ✨ Key Features

- 🍯 **Honeypot Deployment**: Isolated Dockerized Cowrie SSH/Telnet honeypot running on an Oracle Cloud Infrastructure (OCI) VPS.
- 🔄 **Automated ETL Pipeline**: Python script (`analysis/pipeline.py`) that periodically fetches JSON logs via SCP, extracts timestamped login attempts and executed shell commands, and inserts them into MySQL.
- 📊 **Threat Intelligence Analytics**: Aggregates top attacker IP addresses, commonly targeted usernames, brute-force passwords, and executed malicious commands.
- 💻 **Flask Web Dashboard**: Lightweight web application presenting real-time threat metrics, attack counts, and command logs.
- 🔒 **Security-First Design**: Production SSH moved to non-standard ports, key-based authentication enforced, and database credentials decoupled via environment variables (`.env`).

---

## 🚀 Setup & Installation

### 1. Database Setup
Import the database schema into your MySQL instance:
```bash
mysql -u root -p < honeypot_db.sql
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and fill in your VPS SSH and database credentials:
```bash
cp .env.example .env
```
Edit `.env` with your parameters:
```env
VPS_IP=your_vps_ip
VPS_PORT=2222
SSH_KEY=/path/to/your/ssh-key.key
REMOTE_PATH=ubuntu@your_vps_ip:~/honeypot/cowrie-log/cowrie.json
LOCAL_PATH=../data/cowrie.json

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=honeypot_db
```

### 3. Run the Automated Ingestion Pipeline
Start the Python ETL service to fetch logs and sync with MySQL every 5 minutes:
```bash
cd analysis
python pipeline.py
```

### 4. Launch the Web Dashboard
Run the Flask server:
```bash
cd analysis
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to view the dashboard.