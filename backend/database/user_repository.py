from database.db import db
from bson import ObjectId

users_collection = db["users"]


# ============================================================
# CREATE USER
# ============================================================

def create_user(user_data):

    result = users_collection.insert_one(user_data)

    return str(result.inserted_id)


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    users = list(
        users_collection.find()
    )

    for user in users:
        user["_id"] = str(user["_id"])

    return users


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(email):

    return users_collection.find_one({
        "email": email
    })


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(user_id):

    try:
        user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })
    except Exception:
        return None

    if not user:
        return None

    user["_id"] = str(user["_id"])

    return user