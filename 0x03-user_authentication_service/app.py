#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
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
    # if not email or not password:
    #   jsonify({"message": "email and password required"}), 400
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({
            "email": user.email,
            "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


#@app.route('/sessions', methods=['POST'])
#def login() -> str:
#    """ POST /sessions
#    the request expected form data contain:
#        - email
#        - password
#    Returns:
#        - {"email": "<user email>", "message": "logged in"}
#        - abort 401
#    """
#    email = request.form.get("email")
#    password = request.form.get("password")
#    try:
#        if not AUTH.valid_login(email=email, password=password):
#            abort(401)
#        session_id = AUTH.create_session(email=email)
#        response = make_response(jsonify({
#                                   "email": email, "message": "logged in"}))
#        response.set_cookie('session_id', session_id)
#        return response
#    except Exception:
#        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ DELETE /sessions
    the request expected session ID Cookie
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """GET /profile
    the request expected session ID Cookie
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """ POST /reset_password
    the request expected form data with email
    """
    email = request.form.get('email')
    if not email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """PUT /reset_password
    the request expected form data with:
        - email
        - reset_token
        - new_password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
