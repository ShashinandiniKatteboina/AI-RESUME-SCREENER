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

users_bp = Blueprint(
    "users",
    __name__
)


# ============================================================
# GET ALL USERS
# ============================================================

@users_bp.route(
    "/users",
    methods=["GET"]
)
@token_required
def get_users():

    users = get_all_users()

    return jsonify({

        "total_users":
            len(users),

        "users":
            users

    }), 200


# ============================================================
# CREATE USER
# ============================================================

@users_bp.route(
    "/users",
    methods=["POST"]
)
def add_user():

    data = request.get_json()

    if not data:

        return jsonify({
            "error":
                "Request body is required"
        }), 400


    # --------------------------------------------------------
    # Get name
    # --------------------------------------------------------

    name = data.get("name")

    if not name:

        return jsonify({
            "error":
                "name is required"
        }), 400


    # --------------------------------------------------------
    # Get email
    # --------------------------------------------------------

    email = data.get("email")

    if not email:

        return jsonify({
            "error":
                "email is required"
        }), 400


    # --------------------------------------------------------
    # Get password
    # --------------------------------------------------------

    password = data.get("password")

    if not password:

        return jsonify({
            "error":
                "password is required"
        }), 400


    # --------------------------------------------------------
    # Get role
    # --------------------------------------------------------

    role = data.get(
        "role",
        "candidate"
    )


    # --------------------------------------------------------
    # Validate role
    # --------------------------------------------------------

    if role not in [
        "candidate",
        "recruiter"
    ]:

        return jsonify({

            "error":
                "role must be candidate or recruiter"

        }), 400


    # --------------------------------------------------------
    # Check existing user
    # --------------------------------------------------------

    existing_user = get_user_by_email(
        email
    )

    if existing_user:

        return jsonify({

            "error":
                "Email already registered"

        }), 409


    # --------------------------------------------------------
    # Create user data
    # --------------------------------------------------------

    user_data = {

        "name":
            name,

        "email":
            email,

        "password":
            password,

        "role":
            role
    }


    # --------------------------------------------------------
    # Create user
    # --------------------------------------------------------

    inserted_id = create_user(
        user_data
    )


    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return jsonify({

        "message":
            "User created successfully",

        "user_id":
            inserted_id,

        "role":
            role

    }), 201


# ============================================================
# LOGIN
# ============================================================

@users_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    # --------------------------------------------------------
    # Validate request
    # --------------------------------------------------------

    if not data:

        return jsonify({

            "error":
                "Request body is required"

        }), 400


    email = data.get(
        "email"
    )

    password = data.get(
        "password"
    )


    # --------------------------------------------------------
    # Validate email
    # --------------------------------------------------------

    if not email:

        return jsonify({

            "error":
                "email is required"

        }), 400


    # --------------------------------------------------------
    # Validate password
    # --------------------------------------------------------

    if not password:

        return jsonify({

            "error":
                "password is required"

        }), 400


    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = get_user_by_email(
        email
    )

    if not user:

        return jsonify({

            "error":
                "Invalid email or password"

        }), 401


    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    if not verify_password(
        user["password"],
        password
    ):

        return jsonify({

            "error":
                "Invalid email or password"

        }), 401


    # --------------------------------------------------------
    # Get role
    #
    # Existing users that don't have a role will be treated
    # as candidates.
    # --------------------------------------------------------

    role = user.get(
        "role",
        "candidate"
    )


    # --------------------------------------------------------
    # Create JWT payload
    # --------------------------------------------------------

    payload = {

        "user_id":
            str(user["_id"]),

        "email":
            user["email"],

        "role":
            role,

        "exp":
            datetime.now(
                timezone.utc
            ) + timedelta(
                hours=24
            )
    }


    # --------------------------------------------------------
    # Generate JWT
    # --------------------------------------------------------

    token = jwt.encode(

        payload,

        current_app.config[
            "JWT_SECRET_KEY"
        ],

        algorithm="HS256"
    )


    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return jsonify({

        "message":
            "Login successful",

        "token":
            token,

        "user": {

            "id":
                str(user["_id"]),

            "name":
                user["name"],

            "email":
                user["email"],

            "role":
                role
        }

    }), 200