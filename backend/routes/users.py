from flask import Blueprint, jsonify, request

from services.user_service import create_user, get_all_users


users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users():

    users = get_all_users()

    return jsonify(users)


@users_bp.route("/users", methods=["POST"])
def add_user():

    data = request.json

    inserted_id = create_user(data)

    return jsonify({
        "message": "User Created Successfully",
        "id": inserted_id
    }), 201