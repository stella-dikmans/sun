from flask import Flask, request, send_from_directory
from datetime import datetime
import subprocess
import os

# Create the Flask app, telling it where the static files live
app = Flask(__name__, static_folder="static")

PRINTER_NAME = "Jolimark_TP510"

# Route to serve the HTML form (index.html) from the static folder
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Route to handle form submissions and send the print job
@app.route('/print', methods=['POST'])
def print_text():
    content = request.form['text']
    # Add timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"{timestamp}\n{content}\n\n---\n"

    # Write to a temporary file
    with open("printjob.txt", "w") as f:
        f.write(full_message)

    # Send to the printer via lp
    subprocess.run(["lp", "-d", PRINTER_NAME, "printjob.txt"] )

    return "Sent to printer!", 200

if __name__ == '__main__':
    # Ensure working directory is this file's location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app.run(port=5000)
