from database.db import db
from bson import ObjectId


# ============================================================
# SAVE JOB
# ============================================================

def save_job(job_data):

    collection = db["jobs"]

    result = collection.insert_one(job_data)

    return str(result.inserted_id)


# ============================================================
# GET ONE JOB
# ============================================================

def get_job(job_id):

    collection = db["jobs"]

    job = collection.find_one({
        "_id": ObjectId(job_id)
    })

    if job:
        job["_id"] = str(job["_id"])

    return job


# ============================================================
# GET ALL JOBS
# ============================================================

def get_all_jobs():

    collection = db["jobs"]

    jobs = collection.find()

    result = []

    for job in jobs:

        job["_id"] = str(job["_id"])

        result.append(job)

    return result