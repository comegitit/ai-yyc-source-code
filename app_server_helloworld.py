from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/hello")
def hello():
    return "If you can see this message, the front end is communicating with Python in the back end"

# No app.run() — PythonAnywhere loads this via WSGI