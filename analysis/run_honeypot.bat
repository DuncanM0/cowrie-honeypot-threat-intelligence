@echo off
title Honeypot Launcher

echo Starting Honeypot Ingestion Pipeline...
start "Pipeline Backend" cmd /k "cd /d C:\Users\dunca\cowrie-honeypot-threat-intelligence\analysis && python pipeline.py"

echo Starting Flask Dashboard...
start "Flask Frontend" cmd /k "cd /d C:\Users\dunca\cowrie-honeypot-threat-intelligence\analysis && python app.py"

echo Both services launched!