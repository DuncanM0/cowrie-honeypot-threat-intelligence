# Cowrie SSH Honeypot Threat Intelligence

An end-to-end threat intelligence system that runs a **Cowrie SSH/Telnet honeypot** and a **MySQL database** inside Docker on an **Oracle Cloud VPS**, ingests and geolocates attack logs, and displays analytics via a Flask web dashboard enclosed in a native desktop GUI.

---

##  Architecture & How It Works

[![Architecture diagram of duncanm0/cowrie-honeypot-threat-intelligence](https://gitdiagram.com/duncanm0/cowrie-honeypot-threat-intelligence/diagram.png)](https://gitdiagram.com/duncanm0/cowrie-honeypot-threat-intelligence?utm_source=readme&utm_medium=picture)

1. **Honeypot Container (Oracle Cloud VPS)**: Cowrie runs in Docker on an Oracle Cloud Ubuntu 24.04 VM, listening on public port `22` (forwarded internally to `2222` for fake SSH) and `2223` (Telnet). It logs all brute-force attempts, credentials, and commands to `cowrie.json`.
2. **Database Container**: MySQL 8.0 runs via Docker Compose on the same VM (`docker compose up -d db`). Schema initialization (`honeypot_db.sql`) creates tables for `login_attempts` (with IP geolocation fields) and `command_logs`.
3. **Log Processing Pipeline (`pipeline.py`)**: Reads `cowrie.json` incremental logs, enriches attacker IP addresses with geolocation coordinates (Country, City, Lat/Lon) using `ip-api.com`, and writes structured records into MySQL.
4. **Flask Dashboard (`app.py` & `analyze_logs.py`)**: Queries MySQL to display metrics:
   - Total attempts, successful vs failed login counts
   - Top targeted usernames and tried passwords
   - Top attacking IP addresses & country distribution
   - Timeline of login attempts by hour
   - Interactive Folium geographic attack heatmap
5. **One-Click Native Launcher (`launcher.py` / `run_honeypot.bat`)**:
   - Starts MySQL via Docker Compose (`docker compose up -d db`).
   - Waits for database port `3306` to be ready.
   - Launches `pipeline.py` and `app.py` in the background.
   - Opens a native desktop window using `pywebview` pointing to `http://localhost:5000`.

---

##  Project Structure

```
├── docker-compose.yml       # Docker Compose setup for Cowrie & MySQL 8.0
├── honeypot_db.sql          # MySQL database schema
├── .env.example             # Template for environment configuration
├── analysis/
│   ├── run_honeypot.bat     # One-click Windows batch launcher
│   ├── launcher.py          # PyWebView GUI orchestrator (starts Docker DB & app)
│   ├── app.py               # Flask web server & heatmap generator
│   ├── pipeline.py          # Log parser & IP geolocation processor
│   ├── analyze_logs.py      # Database queries & statistics logic
│   ├── config.py            # Environment loader (.env)
│   ├── templates/
│   │   └── index.html       # Web dashboard template
│   └── last_line.txt        # Incremental log offset tracker
└── data/
    └── cowrie.json          # Target path for Cowrie JSON logs
```

---

##  Setup & Installation (Docker Setup)

### 1. Oracle Cloud VPS Setup
On your Oracle Cloud VM (Ubuntu 24.04):
1. Start Cowrie and MySQL containers:
   ```bash
   docker compose up -d
   ```
2. Verify Cowrie is listening on port `22` and MySQL is running on port `3306`.

### 2. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` to configure your database host and paths:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=honeypot_db
LOCAL_PATH=../data/cowrie.json
```

### 3. Running the Application
Double-click **`analysis/run_honeypot.bat`** (or run `python analysis/launcher.py`). This automatically:
- Boots up the MySQL Docker container (`docker compose up -d db`).
- Waits for MySQL on port `3306`.
- Starts the log ingestion pipeline (`pipeline.py`) and Flask web app (`app.py`).
- Launches the desktop application window via PyWebView.

---

## 🔄 Legacy / XAMPP Support (Alternative Setup)

If you prefer using **XAMPP** instead of Docker for the MySQL database:

1. **Update `.env`**:
   Set database credentials for XAMPP (default user is usually `root` with no password):
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=honeypot_db
   ```

2. **Import Database Schema**:
   Open phpMyAdmin (`http://localhost/phpmyadmin`), create a database named `honeypot_db`, and import `honeypot_db.sql`.

3. **Code Changes in `analysis/launcher.py`**:
   In `analysis/launcher.py`, uncomment the XAMPP helpers and replace `start_docker_db()` with `start_xampp()`:

   ```python
   # In analysis/launcher.py:
   XAMPP_SCRIPTS = [r"C:\xampp\apache_start.bat", r"C:\xampp\mysql_start.bat"]

   def start_xampp():
       for file in XAMPP_SCRIPTS:
           p = subprocess.Popen(file, creationflags=CREATE_NO_WINDOW)
           processes.append(p)

   def main():
       atexit.register(stop_all_processes)
       start_xampp()  # Use XAMPP instead of start_docker_db()
       wait_for_port("localhost", 3306, interval=1.5)
       ...
   ```
