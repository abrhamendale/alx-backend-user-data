#!/usr/bin/env python3
"""
Session authentication view module.
"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sess_auth():
    """
    View function for session authentication.
    """
    mail = request.form.get('email')
    p_word = request.form.get('password')
    if mail is None or mail == "":
        return jsonify({"error": "email missing"}), 400
    if p_word is None or p_word == "":
        return jsonify({"error": "password missing"}), 400
    c_user = User.search({'email': mail})
    if c_user:
        c_user = c_user[0]
    if not c_user:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        if not c_user.is_valid_password(p_word):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            s_id = auth.create_session(c_user.id)
            ret_value = jsonify(c_user.to_json())
            c_name = os.getenv('SESSION_NAME')
            ret_value.set_cookie(c_name, s_id)
            return ret_value
    """
    if isinstance(user_pwd, str) is False:
        return None
    emails = User.search({'email': user_email})
    for i in user:
        if i.is_valid_password(p_word):
            pass
    return jsonify({ "error": "wrong password" })
    """


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=True)
def del_user():
    """
    Delete user view function.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
