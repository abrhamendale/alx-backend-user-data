#!/usr/bin/env python3
"""
Session authentication view module.
"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes = False)
def sess_auth():
    """
    View function for session authentication.
    """
    mail = request.form.get('email')
    p_word = request.form.get('password')
    if mail is None or mail == "":
        return jsonify({ "error": "email missing"}), 400
    if p_word is None or p_word == "":
        return jsonify({ "error": "password missing"}), 400
    user = User.search({'email': mail})
    if not user:
        return jsonify({ "error": "no user found for this email"}), 404
    if not user[0].is_valid(p_word):
        return jsonify({ "error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        app.auth.create_session(user[0].id)
        return user[0].to_json()
    """
    if isinstance(user_pwd, str) is False:
        return None
    emails = User.search({'email': user_email})
    for i in user:
        if i.is_valid_password(p_word):
            pass
    return jsonify({ "error": "wrong password" })
    """
