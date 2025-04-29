from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime
import subprocess
import random

app = Flask(__name__)
PRINTER_NAME = "Jolimark_TP510"

# List of possible prompts to show after printing
prompts = [
    "how does it taste?",
    "can you describe my edges?",
    "draw me like one of the moon tales",
    "be my mirror",
    "how close can we really be"
]

@app.route('/')
def index():
    # Get a random prompt (default: "Print Something" if no prompt is passed)
    message = request.args.get('message', random.choice(prompts))
    return render_template_string(open("index.html").read(), message=message)

@app.route('/print', methods=['POST'])
def print_text():
    content = request.form['text']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"{timestamp}\n{content}\n\n---\n"

    with open("printjob.txt", "w") as f:
        f.write(full_message)

    subprocess.run(["lp", "-d", PRINTER_NAME, "printjob.txt"])

    # Redirect back to the form with a new random message
    return redirect(url_for('index', message=random.choice(prompts)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
