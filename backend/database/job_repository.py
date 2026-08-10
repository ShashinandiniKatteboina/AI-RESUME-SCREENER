from database.db import db
from bson import ObjectId


def save_job(job_data):

    collection = db["jobs"]

    result = collection.insert_one(job_data)

    return str(result.inserted_id)


def get_job(job_id):

    collection = db["jobs"]

    job = collection.find_one({
        "_id": ObjectId(job_id)
    })

    return job