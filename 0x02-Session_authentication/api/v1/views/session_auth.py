#!/usr/bin/env python3
"""
Session authentication view module.
"""


@app.route('/auth_session/login', methods=['POST'], strict_slashes = False)
def sess_auth(request = None):
    """
    View function for session authentication.
    """
    mail = request.form.get('email')
    p_word = request.form.get('password')
    if mail is None or mail = "":
        return jsonify({ "error": "email missing" })
    if p_word is None or p_word = "":
        return jsonify({ "error": "password missing" })
    user = User.search({"email": mail})
    if not user:
        return jsonify({ "error": "no user found for this email" })
    if not user.is_valid(p_word):
        return jsonify({ "error": "wrong password" })

