# Cowrie SSH Honeypot Threat Intelligence Lab

## Overview
Deployed a Cowrie SSH/Telnet honeypot on Oracle Cloud Always Free tier to capture and analyse automated attack traffic.

## Architecture

Internet
   |
Oracle Cloud VM
   |
Port 22
   |
Cowrie Docker Container
   |
JSON Event Logs
   |
Python Analysis

## Technologies
- Oracle Cloud Infrastructure
- Ubuntu 24.04
- Docker
- Cowrie Honeypot
- Python

## Security Controls
- Real SSH moved to port 2222
- Password authentication disabled
- Network firewall rules configured
- Honeypot isolated in Docker

## Results
(Data analysis coming after collection period)