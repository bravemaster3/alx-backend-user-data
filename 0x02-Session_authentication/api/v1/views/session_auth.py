#!/usr/bin/env python3
"""session auth views"""
from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login method"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    user_json = user.to_json()

    response = make_response(user_json)
    response.set_cookie(os.getenv('SESSION_NAME', '_my_session_id'),
                        session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """logout method"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
