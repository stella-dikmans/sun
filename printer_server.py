from flask import Flask, request, send_from_directory
from datetime import datetime
import subprocess
import os

app = Flask(__name__)
PRINTER_NAME = "Jolimark_TP510"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # Serve index.html from current directory

@app.route('/print', methods=['POST'])
def print_text():
    content = request.form['text']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"{timestamp}\n{content}\n\n---\n"

    # Save to temp file
    with open("printjob.txt", "w") as f:
        f.write(full_message)

    # Send to printer
    subprocess.run(["lp", "-d", PRINTER_NAME, "printjob.txt"])
    return "Sent to printer!"

if __name__ == '__main__':
    app.run(port=5000)