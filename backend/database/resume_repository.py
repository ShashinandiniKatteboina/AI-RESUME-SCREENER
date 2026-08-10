from database.db import db


def save_resume(resume_data):

    collection = db["resumes"]

    result = collection.insert_one(resume_data)

    return str(result.inserted_id)

def get_resume(resume_id):

    from bson import ObjectId

    collection = db["resumes"]

    resume = collection.find_one({
        "_id": ObjectId(resume_id)
    })

    return resume