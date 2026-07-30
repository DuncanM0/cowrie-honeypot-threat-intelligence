from flask import Flask, render_template
import mysql.connector
from analyze_logs import (
    get_top_usernames, get_top_passwords, get_top_ips, get_top_commands,
    get_attempts_by_hour, get_total_login_attempts,
    get_total_successful_logins, get_total_failed_logins
)
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

@app.route("/")
def home():
    return render_template(
        "index.html",
        usernames=get_top_usernames(db),
        passwords=get_top_passwords(db),
        ips=get_top_ips(db),
        commands=get_top_commands(db),
        hours=get_attempts_by_hour(db),
        total_attempts=get_total_login_attempts(db)[0][0],
        total_success=get_total_successful_logins(db)[0][0],
        total_failed=get_total_failed_logins(db)[0][0]
    )

if __name__ == "__main__":
    app.run(debug=True)