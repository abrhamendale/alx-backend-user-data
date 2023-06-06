#!/usr/bin/env python3
"""
App class.
"""


from flask import Flask, request, jsonify
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


if __name__ == "__main__":
        app.run(host="0.0.0.0", port="5000")
