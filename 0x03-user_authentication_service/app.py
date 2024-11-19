#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask


app = Flask(__name__)


@app.rout('/', methods=['GET'])
def get():
    flask.jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
