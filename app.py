from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/hello")
def hello():
    return "If you can see this message, the front end is communicating with Python in the back end"

@app.route("/")
def index():
    return render_template("index.html", title="Home")

@app.route("/webdev")
def webdev():
    return render_template("webdev.html", title="Web Dev")

# No app.run() — PythonAnywhere loads this via WSGI