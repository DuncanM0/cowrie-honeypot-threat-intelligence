import json

logins = []

total_successful_logins = 0
total_failed_logins = 0
total_login_attempts = 0


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
            
            logins.append({
                "username": event["username"],
                "password": event["password"],
                "ip": event["src_ip"],
                "time": event["timestamp"],
                "session": event["session"],
                "status": "failed"
                })


for item in logins:
    if item["status"] == "success":
        total_successful_logins += 1
    elif item["status"] == "failed":
        total_failed_logins += 1

username_counts = count_values(logins, "username")
password_counts = count_values(logins, "password")
ip_counts = count_values(logins, "ip")
total_login_attempts = len(logins)

print(f"Username count: {username_counts}")
print(f"Password count: {password_counts}")
print(f"IP count: {ip_counts}")
print(f"Total Login count: {total_login_attempts}")
print(f"Total Successful Login count: {total_successful_logins}")
print(f"Total Failed Login count: {total_failed_logins}")

        
    


