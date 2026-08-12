from database.db import db

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ============================================================
# USERS COLLECTION
# ============================================================

users_collection = db["users"]


# ============================================================
# CREATE USER
# ============================================================

def create_user(user_data):

    password = user_data.get("password")

    hashed_password = generate_password_hash(
        password
    )

    user_document = {
        "name": user_data.get("name"),
        "email": user_data.get("email"),
        "password": hashed_password
    }

    result = users_collection.insert_one(
        user_document
    )

    return str(result.inserted_id)


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    users = list(
        users_collection.find(
            {},
            {
                "password": 0
            }
        )
    )

    for user in users:
        user["_id"] = str(user["_id"])

    return users


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(email):

    user = users_collection.find_one({
        "email": email
    })

    return user


# ============================================================
# VERIFY PASSWORD
# ============================================================

def verify_password(
    stored_password,
    entered_password
):

    return check_password_hash(
        stored_password,
        entered_password
    )