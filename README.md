# Cowrie SSH Honeypot Threat Intelligence

This project runs a Cowrie SSH/Telnet honeypot on an Oracle Cloud VPS (Ubuntu 24.04 in Docker) to capture and analyze automated brute-force attacks and malicious commands.

It includes a Python pipeline to pull logs from the VPS into a MySQL database, along with a Flask web dashboard to view top attacker IPs, credentials tried, and commands run.

## Project Structure

- `analysis/app.py` - Flask web dashboard for viewing attack statistics
- `analysis/pipeline.py` - Automated script to fetch logs via SCP and store them in MySQL
- `analysis/analyze_logs.py` - Data parsing, SQL queries, and Matplotlib graphs
- `analysis/config.py` - Environment configuration loader
- `analysis/templates/index.html` - Dashboard template
- `docker-compose.yml` - Docker compose file to run Cowrie
- `honeypot_db.sql` - Database schema

## Setup

1. **Database:** Import `honeypot_db.sql` into MySQL:
   ```bash
   mysql -u root -p < honeypot_db.sql
   ```

2. **Environment Variables:** Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```

3. **Log Pipeline:** Run the pipeline script to fetch logs and store them in MySQL:
   ```bash
   cd analysis
   python pipeline.py
   ```

4. **Web Dashboard:** Start the Flask app:
   ```bash
   cd analysis
   python app.py
   ```