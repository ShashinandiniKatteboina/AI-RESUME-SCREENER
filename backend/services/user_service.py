from database.db import db


users_collection = db["users"]


def create_user(user_data):

    result = users_collection.insert_one(user_data)

    return str(result.inserted_id)


def get_all_users():

    users = list(users_collection.find())

    for user in users:
        user["_id"] = str(user["_id"])

    return users