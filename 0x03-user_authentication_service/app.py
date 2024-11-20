#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth
from typing import Dict


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def get():
    """ Get /
    Return:
        - JSON {"message" : "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """ POST /users
    Return:
        - if not registered:
            {"email": "<registered email>", "message": "user created"}
        - if already registered:
            {"message": "email already registered"}, 400
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        jsonify({"message": "email and password required"}), 400
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({
            "email": user.email,
            "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """ POST /sessions
    the request expected form data contain:
        - email
        - password
    Returns:
        - {"email": "<user email>", "message": "logged in"}
        - abort 401
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(401)
    try:
        AUTH.valid_login(email=email, password=password)
        session_id = AUTH.create_session(email=email)
        response = make_response(jsonify({
                                    "email": email, "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response
    except Exception:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
