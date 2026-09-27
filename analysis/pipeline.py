import os
import time
import mysql.connector
import requests
from analyze_logs import (
    insert_login, insert_command
)
import json
from datetime import datetime
from config import (
    LOCAL_PATH,
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
)

geo_cache = {}
OFFSET_FILE = "last_line.txt"

def get_last_offset():
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                return int(content)
    return 0

def save_last_offset(line_number):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(line_number))

def get_geoip(ip):
    if ip in geo_cache:
        return geo_cache[ip]
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        if data.get("status") == "success":
            geo = {
                "country": data.get("country"),
                "city": data.get("city"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }
        else:
            geo = {"country": None, "city": None, "lat": None, "lon": None}
    except requests.RequestException:
        geo = {"country": None, "city": None, "lat": None, "lon": None}
    geo_cache[ip] = geo
    return geo

def parse_and_store():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    last_offset = get_last_offset()
    current_line = 0

    if os.path.exists(LOCAL_PATH):
        with open(LOCAL_PATH) as f:
            for line in f:
                current_line += 1
                if current_line <= last_offset:
                    continue

                event = json.loads(line)
                raw_time = event["timestamp"].replace("Z", "")
                dt = datetime.fromisoformat(raw_time)
                sql_time = dt.strftime('%Y-%m-%d %H:%M:%S')

                if event["eventid"] in ("cowrie.login.success", "cowrie.login.failed"):
                    geo = get_geoip(event["src_ip"])
                    status = "success" if event["eventid"] == "cowrie.login.success" else "failed"
                    insert_login(db, {
                        "session": event["session"], "ip": event["src_ip"], "time": sql_time,
                        "username": event.get("username", ""), "password": event.get("password", ""),
                        "status": status,
                        "country": geo["country"],
                        "city": geo["city"],
                        "lat": geo["lat"],
                        "lon": geo["lon"]
                    })
                elif event["eventid"] == "cowrie.command.input":
                    insert_command(db, {
                        "session": event["session"], "ip": event["src_ip"], "time": sql_time,
                        "command": event["input"]
                    })
    else:
        print(f"WARNING: log file not found at {LOCAL_PATH}")

    db.commit()
    db.close()

    print("saving Offset")
    save_last_offset(current_line)
    print("Data inserted into MySQL.")

if __name__ == "__main__":
    try:
        while True:
            parse_and_store()
            with open("last_updated.txt", "w") as f:
                f.write(datetime.now().isoformat())
            print("Recording time...\n")
            print("Sleeping for 5 minutes...\n")
            time.sleep(300)
    except KeyboardInterrupt:
        print("\n[!] Ctrl+C detected. Shutting down ...")