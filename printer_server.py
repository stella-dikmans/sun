from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime
import subprocess

app = Flask(__name__)
PRINTER_NAME = "Jolimark_TP510"

@app.route('/')
def index():
    message = request.args.get('message', 'Print Something')
    return render_template_string(open("index.html").read(), message=message)

@app.route('/print', methods=['POST'])
def print_text():
    content = request.form['text']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"{timestamp}\n{content}\n\n---\n"

    with open("printjob.txt", "w") as f:
        f.write(full_message)

    subprocess.run(["lp", "-d", PRINTER_NAME, "printjob.txt"])

    # 👇 This makes the browser go back to the form, with a new message!
    return redirect(url_for('index', message="Printed!"))

if __name__ == '__main__':
    app.run(port=5000)