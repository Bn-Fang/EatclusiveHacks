

from flask import Flask
app = Flask(__name__)

@app.route("/")

def index():
    return "this is a test!"
app.run(host="0.0.0.0", port = 80 )
