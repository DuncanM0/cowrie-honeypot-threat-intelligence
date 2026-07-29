The honeypot runs as a Docker container on an Oracle Cloud VM.



Incoming SSH scans reach port 22, which is forwarded to Cowrie's fake SSH service.



The real server administration SSH service runs separately on port 2222.

