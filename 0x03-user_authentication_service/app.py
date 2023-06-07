#!/usr/bin/env python3
"""
App class.
"""


from flask import Flask, request, abort, jsonify, make_response, redirect
from flask import url_for
from auth import Auth
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def unauthorized(error) -> str:
    """
    Unauthorized handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.route('/', methods=['GET'], strict_slashes=False)
def route_1():
    """
    A route.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    Registers users from request form.
    """
    em = request.form.get("email")
    p_w = request.form.get("password")
    try:
        user = AUTH.register_user(em, p_w)
        return jsonify({"email": em, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Login route function.
    """
    em: str = request.form.get("email")
    p_w: str = request.form.get("password")
    if not AUTH.valid_login(em, p_w):
        abort(401)
    else:
        s_id: str = AUTH.create_session(em)
        resp = make_response({"email": em, "message": "logged in"})
        resp.set_cookie('session_id', str(s_id))
        return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out a user.
    """
    s_id: str = request.cookie.get("session_id")
    try:
        usr = self._db.find_user_by(session_id=s_id)
        AUTH.destroy_session(usr.session_id)
        return redirect(url_for('route_1'))
    except NoResultFound:
        return jsonify({}), 403


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    /profile route handler.
    """
    s_id: str = request.cookies.get("session_id")
    try:
        usr = AUTH._db.find_user_by(session_id=s_id)
        return jsonify({"email": usr.email}), 200
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Function to respond to the POST /reset_password route.
    """
    em: str = request.form.get("email")
    try:
        usr: User = AUTH._db.find_user_by(email=em)
        r_t: str = Auth._db.get_reset_password_token(em)
        return jsonify({"email": em, "reset_token": r_t}), 200
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Function to respond to PUT /reset_password.
    """
    try:
        r_t: str = request.form.get("reset_token")
        p_w: str = request.form.get("new_password")
        e_m: str = request.form.get("email")
        AUTH._db.update_password(r_t, p_w)
        return jsonify({"email": e_m, "message": "Password updated"}), 200
    except NoResultFound:
        return "Forbidden", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
