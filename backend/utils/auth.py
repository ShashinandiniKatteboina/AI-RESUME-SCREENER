from functools import wraps
from flask import request, jsonify, current_app
import jwt


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

        if len(parts) != 2 or parts[0].lower() != "bearer":
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

            # ------------------------------------------------
            # Store logged-in user's information
            # ------------------------------------------------

            request.user_id = payload["user_id"]
            request.user_email = payload.get("email")

        except jwt.ExpiredSignatureError:

            return jsonify({
                "error": "Token has expired"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "error": "Invalid token"
            }), 401

        # ----------------------------------------------------
        # Token valid → continue to route
        # ----------------------------------------------------

        return f(*args, **kwargs)

    return decorated