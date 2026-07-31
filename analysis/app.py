from flask import Flask, render_template
import mysql.connector
import folium
from folium.plugins import HeatMap
from analyze_logs import (
    get_top_usernames, get_top_passwords, get_top_ips, get_top_commands,
    get_attempts_by_hour, get_total_login_attempts,
    get_total_successful_logins, get_total_failed_logins,
    get_top_countries
)
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_heatmap(db):
    cursor = db.cursor()
    points = []

    cursor.execute("""
        SELECT lat, lon
        FROM login_attempts
        WHERE lat IS NOT NULL
        AND lon IS NOT NULL
    """)

    locations = cursor.fetchall()

    m = folium.Map(
        location=[20,0],
        zoom_start=2,
        width="1200px",
        height="800px",
        zoom_control=False,
        scrollWheelZoom=False,
        dragging=False
    )

    for lat, lon in locations:
        points.append([lat, lon])

    HeatMap(points).add_to(m)
    return m._repr_html_()

@app.route("/last-updated")
def last_updated():
    with open("last_updated.txt") as f:
        return f.read()

@app.route("/")
def home():

    db = get_db()
    map_html = create_heatmap(db)


    return render_template(
        "index.html",
        usernames=get_top_usernames(db),
        passwords=get_top_passwords(db),
        ips=get_top_ips(db),
        commands=get_top_commands(db),
        countries=get_top_countries(db),
        hours=get_attempts_by_hour(db),
        total_attempts=get_total_login_attempts(db)[0][0],
        total_success=get_total_successful_logins(db)[0][0],
        total_failed=get_total_failed_logins(db)[0][0],
        map_html=map_html
    )



if __name__ == "__main__":
    app.run(debug=True)