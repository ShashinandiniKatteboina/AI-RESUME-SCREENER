from functools import wraps

from flask import request, jsonify, current_app

import jwt

from database.user_repository import get_user_by_id


# ============================================================
# JWT TOKEN REQUIRED
# ============================================================

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        # ----------------------------------------------------
        # Get Authorization header
        # ----------------------------------------------------

        auth_header = request.headers.get("Authorization")

        if not auth_header:

            return jsonify({
                "error": "Authorization header is required"
            }), 401

        # ----------------------------------------------------
        # Check Bearer format
        # ----------------------------------------------------

        parts = auth_header.split()

        if (
            len(parts) != 2
            or parts[0].lower() != "bearer"
        ):

            return jsonify({
                "error": "Authorization header must be Bearer <token>"
            }), 401

        token = parts[1]

        # ----------------------------------------------------
        # Verify JWT
        # ----------------------------------------------------

        try:

            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:

            return jsonify({
                "error": "Token has expired"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "error": "Invalid token"
            }), 401

        # ----------------------------------------------------
        # Get user ID from token
        # ----------------------------------------------------

        user_id = payload.get("user_id")

        if not user_id:

            return jsonify({
                "error": "Invalid token payload"
            }), 401

        # ----------------------------------------------------
        # Check whether user still exists
        # ----------------------------------------------------

        user = get_user_by_id(user_id)

        if not user:

            return jsonify({
                "error": "User no longer exists"
            }), 401

        # ----------------------------------------------------
        # Store authenticated user information
        # ----------------------------------------------------

        request.user_id = user_id

        request.user_email = payload.get("email")

        request.current_user = user

        # ----------------------------------------------------
        # Continue to requested route
        # ----------------------------------------------------

        return f(*args, **kwargs)

    return decorated