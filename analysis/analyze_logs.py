import json
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime


logins = []
commands = []
time = []

total_successful_logins = 0
total_failed_logins = 0
total_login_attempts = 0


def get_value(item):
    return item[1]

def create_bar_graph(data, title, x_label, y_label):
    labels = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def count_values(data, key):
    counts = {}

    for item in data:
        value = item[key]

        if value in counts:
            counts[value] += 1
        else:
            counts[value] = 1

    return counts

def insert_login(db, data):
    cursor = db.cursor()
    cursor.execute(
        "INSERT IGNORE INTO login_attempts (session_id, src_ip, timestamp, username, password, status, country, city, lat, lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (data["session"], data["ip"], data["time"], data["username"], data["password"], data["status"],  data["country"], data["city"], data["lat"], data["lon"])
        )
    cursor.close()
    db.commit()


def insert_command(db, data):
    cursor = db.cursor()
    cursor.execute(
        "INSERT IGNORE INTO command_logs (session_id, src_ip, timestamp, command_input) Values (%s, %s, %s, %s)",
        (data["session"], data["ip"], data["time"], data["command"])
        )
    cursor.close()
    db.commit()



def get_top_usernames(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT username, COUNT(*) as attempts FROM login_attempts GROUP BY username ORDER BY attempts DESC LIMIT 10"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_top_passwords(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT password, COUNT(*) as attempts FROM login_attempts GROUP BY password ORDER BY attempts DESC LIMIT 10"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_top_ips(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT src_ip, COUNT(*) as attempts FROM login_attempts GROUP BY src_ip ORDER BY attempts DESC LIMIT 10"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_top_commands(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT command_input, COUNT(*) as attempts FROM command_logs GROUP BY command_input ORDER BY attempts DESC LIMIT 10"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_top_countries(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT country, COUNT(*) as attempts FROM login_attempts GROUP BY country ORDER BY attempts DESC LIMIT 10"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_attempts_by_hour(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT HOUR(timestamp) as hour, COUNT(*) as attempts FROM login_attempts GROUP BY hour ORDER BY hour;"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_attempts_by_day(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT DAY(timestamp) as day, COUNT(*) as attempts FROM login_attempts GROUP BY day ORDER BY day;"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_total_login_attempts(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM login_attempts;"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_total_successful_logins(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM login_attempts WHERE status = 'success';"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

def get_total_failed_logins(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM login_attempts WHERE status = 'failed';"
    )
    results = cursor.fetchall()
    cursor.close()
    return results

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, LOCAL_PATH

if __name__ == "__main__":
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    with open(LOCAL_PATH) as f:
        for line in f:
            event = json.loads(line)

            raw_time = event["timestamp"].replace("Z", "")
            dt = datetime.fromisoformat(raw_time)
            sql_time = dt.strftime('%Y-%m-%d %H:%M:%S')

            #If login succesful store username and password attempted to use
            if event["eventid"] == "cowrie.login.success":

                total_successful_logins += 1

                insert_login(db, {
                    "session": event["session"],
                    "ip": event["src_ip"],
                    "time": sql_time,
                    "username": event["username"],
                    "password": event.get("password", ""),
                    "status": "success",
                    "country": None,
                    "city": None,
                    "lat": None,
                    "lon": None
                    })

                
                logins.append({
                    "username": event["username"],
                    "password": event.get("password", ""),
                    "ip": event["src_ip"],
                    "time": event["timestamp"],
                    "session": event["session"],
                    "status": "success"
                    })
                    
                

             #If login failed store username and password attempted to use
            elif event["eventid"] == "cowrie.login.failed":

                insert_login(db, {
                    "session": event["session"],
                    "ip": event["src_ip"],
                    "time": sql_time,
                    "username": event["username"],
                    "password": event.get("password", ""),
                    "status": "failed",
                    "country": None,
                    "city": None,
                    "lat": None,
                    "lon": None
                    })

                
                total_failed_logins += 1
                logins.append({
                    "username": event["username"],
                    "password": event.get("password", ""),
                    "ip": event["src_ip"],
                    "time": event["timestamp"],
                    "session": event["session"],
                    "status": "failed"
                    })
                

            #If command was inputted
            elif event["eventid"] == "cowrie.command.input":

                insert_command(db, {
                    "session": event["session"],
                    "ip": event["src_ip"],
                    "time": sql_time,
                    "command": event["input"],
                    })

                
                commands.append({
                    "session": event["session"],
                    "ip": event["src_ip"],
                    "time": event["timestamp"],
                    "command": event["input"]
                    })
                



    for item in logins:
        dt = datetime.fromisoformat(item["time"])
        time.append({"day": dt.day, "hour": dt.hour})


    command_counts = count_values(commands, "command")       
    hour_counts = count_values(time, "hour")
    day_counts = count_values(time, "day")
    username_counts = count_values(logins, "username")
    password_counts = count_values(logins, "password")
    ip_counts = count_values(logins, "ip")
    total_login_attempts = len(logins)

    top_10_ips = dict(sorted(ip_counts.items(), key=get_value, reverse=True)[:10])
    top_10_passwords = dict(sorted(password_counts.items(), key=get_value, reverse=True)[:10])
    top_10_usernames = dict(sorted(username_counts.items(), key=get_value, reverse=True)[:10])
    top_10_commands = dict(sorted(command_counts.items(), key=get_value, reverse=True)[:10])



    create_bar_graph(top_10_usernames,
                     "Username Attempts",
                     "Username",
                     "Attempts")

    create_bar_graph(top_10_passwords,
                     "Password Attempts",
                     "Password",
                     "Attempts")

    create_bar_graph(top_10_ips,
                     "Source IP Addresses",
                     "IP Address",
                     "Attempts")

    create_bar_graph(top_10_commands,
                     "Commands Executed",
                     "Command",
                     "Count")

    print(f"Username count: {username_counts}")
    print(f"Password count: {password_counts}")
    print(f"IP count: {ip_counts}")
    print(f"Total Login count: {total_login_attempts}")
    print(f"Total Successful Login count: {total_successful_logins}")
    print(f"Total Failed Login count: {total_failed_logins}")
    print(f"Day count: {day_counts}")
    print(f"Hour count: {hour_counts}")
    print(f"Command count: {command_counts}")