from database.db import db


def save_resume(resume_data):

    collection = db["resumes"]

    result = collection.insert_one(resume_data)

    return str(result.inserted_id)