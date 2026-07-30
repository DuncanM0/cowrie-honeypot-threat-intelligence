import os
from pathlib import Path

def load_env():
    """Load key-value pairs from .env into os.environ if present."""
    base_dir = Path(__file__).resolve().parent
    env_paths = [base_dir / ".env", base_dir.parent / ".env"]
    
    for env_path in env_paths:
        if env_path.is_file():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip("'\"")
                        if key and key not in os.environ:
                            os.environ[key] = val
            break

load_env()

# VPS Configuration
VPS_IP = os.getenv("VPS_IP", "127.0.0.1")
VPS_PORT = os.getenv("VPS_PORT", "2222")
SSH_KEY = os.getenv("SSH_KEY", "ssh-key.key")
REMOTE_PATH = os.getenv("REMOTE_PATH", f"ubuntu@{VPS_IP}:~/honeypot/cowrie-log/cowrie.json")
LOCAL_PATH = os.getenv("LOCAL_PATH", "../data/cowrie.json")

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "honeypot_db")
