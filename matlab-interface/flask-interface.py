from flask import Flask

app = Flask(__name__)

@app.route("/<filename>")
def request_received(filename):
    return f"<br><b>Got file {filename}</b><br>"
