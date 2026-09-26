# Cowrie SSH Honeypot Threat Intelligence

This project runs a Cowrie SSH/Telnet honeypot on an Oracle Cloud VPS (Ubuntu 24.04 in Docker) to capture and analyze automated brute-force attacks and malicious commands.

It includes a Python pipeline to pull logs from the VPS into a MySQL database, along with a Flask web dashboard to view top attacker IPs, credentials tried, and commands run.

## Project Structure

- `analysis/launcher.py` - Starts XAMPP, waits for MySQL, runs the pipeline and dashboard, and opens the app in a desktop window
- `analysis/run_honeypot.bat` - One-click entry point that runs `launcher.py`
- `analysis/app.py` - Flask web dashboard for viewing attack statistics
- `analysis/pipeline.py` - Automated script to fetch logs via SCP and store them in MySQL
- `analysis/analyze_logs.py` - Data parsing, SQL queries, and Matplotlib graphs
- `analysis/config.py` - Environment configuration loader
- `analysis/templates/index.html` - Dashboard template
- `docker-compose.yml` - Docker compose file to run Cowrie
- `honeypot_db.sql` - Database schema

## Setup

1. **Database:** Import `honeypot_db.sql` into MySQL via phpMyAdmin inside XAMPP (`http://localhost/phpmyadmin`).

2. **Environment Variables:** Copy `.env.example` to `.env` and fill in your details:
```bash
   cp .env.example .env
```

3. **Run everything:** Double-click `run_honeypot.bat` (or run `analysis/launcher.py` directly). This starts XAMPP, waits for MySQL to come up, runs the log pipeline, starts the Flask dashboard, and opens it in a desktop window automatically.

   > `pipeline.py` and `app.py` can still be run individually for debugging, but `run_honeypot.bat` is the intended way to start the full project.