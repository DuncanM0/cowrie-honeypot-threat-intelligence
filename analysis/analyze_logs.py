import json
import matplotlib.pyplot as plt
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


with open('../data/cowrie.json') as f:
    for line in f:
        event = json.loads(line)

        #If login succesful store username and password attempted to use
        if event["eventid"] == "cowrie.login.success":
            total_successful_logins += 1
            logins.append({
                "username": event["username"],
                "password": event["password"],
                "ip": event["src_ip"],
                "time": event["timestamp"],
                "session": event["session"],
                "status": "success"
                })

         #If login failed store username and password attempted to use
        elif event["eventid"] == "cowrie.login.failed":
            total_failed_logins += 1
            logins.append({
                "username": event["username"],
                "password": event["password"],
                "ip": event["src_ip"],
                "time": event["timestamp"],
                "session": event["session"],
                "status": "failed"
                })

        #If command was inputted
        elif event["eventid"] == "cowrie.command.input":
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

        
    


