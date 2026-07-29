# Cowrie Honeypot Setup Notes

## Project Goal

Built an SSH/Telnet honeypot using Cowrie running inside Docker on an Oracle Cloud Always Free Ubuntu VM.

Purpose:
- Capture automated SSH attacks from the internet
- Record login attempts and attacker behaviour
- Analyse attack trends for a cybersecurity portfolio project

---

# Oracle Cloud VM

Provider:
Oracle Cloud Always Free Tier

Operating System:
Ubuntu 24.04

Instance:
VM.Standard.A1.Flex

Resources:
- 1 OCPUs
- 1GB RAM
- 50GB storage

Access:
SSH key authentication

---

# Server Configuration

Connected using:

```bash
ssh -i <private-key> ubuntu@<instance-ip>