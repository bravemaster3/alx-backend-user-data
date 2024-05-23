#!/usr/bin/env python3
"""session auth views"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth


@app_views.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search(email=email)
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.user_id)

    user_json = user.to_json()

    response = make_response(user_json)
    response.set_cookie(auth.session_cookie_name, session_id)

    return response
