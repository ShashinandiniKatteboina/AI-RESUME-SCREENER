from flask import Blueprint, jsonify, request, current_app
from utils.auth import token_required
import jwt
from datetime import datetime, timedelta, timezone

from services.user_service import (
    create_user,
    get_all_users,
    get_user_by_email,
    verify_password
)


# ============================================================
# BLUEPRINT
# ============================================================

users_bp = Blueprint("users", __name__)


# ============================================================
# GET ALL USERS
# ============================================================

@users_bp.route("/users", methods=["GET"])
@token_required
def get_users(user_id):

    users = get_all_users()

    return jsonify({
        "total_users": len(users),
        "users": users
    }), 200


# ============================================================
# CREATE USER
# ============================================================

@users_bp.route("/users", methods=["POST"])
def add_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")

    if not name:
        return jsonify({
            "error": "name is required"
        }), 400

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "email is required"
        }), 400

    password = data.get("password")

    if not password:
        return jsonify({
            "error": "password is required"
        }), 400

    # --------------------------------------------------------
    # Create user
    # --------------------------------------------------------

    user_data = {
        "name": name,
        "email": email,
        "password": password
    }

    inserted_id = create_user(user_data)

    return jsonify({
        "message": "User created successfully",
        "user_id": inserted_id
    }), 201


# ============================================================
# LOGIN
# ============================================================

@users_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    # --------------------------------------------------------
    # Validate request
    # --------------------------------------------------------

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    # --------------------------------------------------------
    # Validate email
    # --------------------------------------------------------

    if not email:
        return jsonify({
            "error": "email is required"
        }), 400

    # --------------------------------------------------------
    # Validate password
    # --------------------------------------------------------

    if not password:
        return jsonify({
            "error": "password is required"
        }), 400

    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = get_user_by_email(email)

    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    if not verify_password(
        user["password"],
        password
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # --------------------------------------------------------
    # Create JWT payload
    # --------------------------------------------------------

    payload = {
        "user_id": str(user["_id"]),
        "email": user["email"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    # --------------------------------------------------------
    # Generate JWT
    # --------------------------------------------------------

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )

    # --------------------------------------------------------
    # Return token
    # --------------------------------------------------------

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }), 200