from database.db import db


def save_analysis(analysis_data):

    collection = db["analyses"]

    result = collection.insert_one(analysis_data)

    return str(result.inserted_id)