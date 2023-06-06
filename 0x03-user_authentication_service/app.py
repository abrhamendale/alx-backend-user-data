#!/usr/bin/env python3
"""
App class.
"""


from flask import Flask, request, jsonify, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


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
        return jsonify({"email": "<registered email>", "message": "user created"})
    except:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Login route function.
    """
    em = request.form.get("email")
    p_w = request.form.get("password")
    print("eeemmmaaiiill", em, p_w)
    if not AUTH._db.find_user_by(email = em):
        abort(401)
    else:
        s_id = AUTH.create_session(em)
        resp = make_response({"email": em, "message": "logged in"})
        resp.set_cookie('session_id', str(s_id))
        return resp
        #return jsonify({"email": em, "message": "logged in"})


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out a user.
    """
    s_id = request.cookie.get("session_id")
    if not AUTH._db.find_user_by(session_id = s_id):
        abort(403)
    else:
        AUTH.destroy_session(s_id)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    /profile route handler.
    """
    s_id = request.cookies.get("session_id")
    usr = AUTH._db.find_user_by(session_id = s_id)
    if not usr:
        abort(403)
    else:
        return jsonify({"email": usr.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    Function to respond to the POST /reset_password route.
    """
    em = requests.form.get("email")
    try:
        usr = AUTH._db.find_user_by("email" = em)
        r_t = Auth.get_reset_password_token(em)
        return jsonify({"email": em, "reset_token": r_t})
    except NotFoundError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    Function to respond to PUT /reset_password.
    """
    try:
        r_t = requests.form.get("reset_token")
        p_w = requests.form.get("new_password")
        e_m = requests.form.get("email")
        AUTH._db.update_password(r_t, p_w)
        return jsonify({"email": e_m, "message": "Password updated"}), 200
    except NoResultFound:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
