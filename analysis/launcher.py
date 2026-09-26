import atexit
import webview
import os
import socket
import subprocess
import time
from contextlib import closing

CREATE_NO_WINDOW = 0x08000000

XAMPP_SCRIPTS = [r"C:\xampp\apache_start.bat", r"C:\xampp\mysql_start.bat"]
                 
XAMPP_STOP_SCRIPTS = [r"C:\xampp\apache_stop.bat", r"C:\xampp\mysql_stop.bat"]

processes = []
   
def check_socket(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return bool (1)
        else:
            return bool (0)

def start_xampp():
    for file in XAMPP_SCRIPTS:
        p = subprocess.Popen(file, creationflags=CREATE_NO_WINDOW)
        processes.append(p)

def wait_for_port(host, port, interval=1.0):
    while not check_socket(host, port):
        print(f"waiting for {host}:{port}...")
        time.sleep(interval)

def start_app():
    p1 = subprocess.Popen(["python", "pipeline.py"], creationflags=CREATE_NO_WINDOW)
    p2 = subprocess.Popen(["python", "app.py"], creationflags=CREATE_NO_WINDOW)
    processes.extend([p1,p2])

def stop_all_processes():
    for file in XAMPP_STOP_SCRIPTS:
        subprocess.Popen(file, creationflags=CREATE_NO_WINDOW)

    time.sleep(1)

    print("Stopping all processes now ... ")
    for p in processes:
        if p.poll() == None:
            p.terminate()

    time.sleep(1)

    for p in processes:
        if p.poll() is None:
            p.kill()

def main():
    atexit.register(stop_all_processes)
    start_xampp()

    wait_for_port("localhost", 3306, interval=1.5)
    print("MySQL is up, launching pipeline and app")

    start_app()

    wait_for_port("127.0.0.1", 5000, interval=0.5)

    window = webview.create_window('Honeypot Dashboard', 'http://localhost:5000')
    window.events.closing += stop_all_processes
    webview.start()

if __name__ == "__main__":
    main()