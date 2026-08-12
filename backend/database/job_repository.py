from database.db import db
from bson import ObjectId

jobs_collection = db["jobs"]


# ============================================================
# SAVE JOB
# ============================================================

def save_job(job_data):

    result = jobs_collection.insert_one(job_data)

    return str(result.inserted_id)


# ============================================================
# GET ONE JOB
# ============================================================

def get_job(job_id):

    try:
        job = jobs_collection.find_one({
            "_id": ObjectId(job_id)
        })
    except Exception:
        return None

    if not job:
        return None

    job["_id"] = str(job["_id"])

    return job


# ============================================================
# GET ALL JOBS
# ============================================================

def get_all_jobs():

    jobs = list(
        jobs_collection.find()
    )

    for job in jobs:
        job["_id"] = str(job["_id"])

    return jobs


# ============================================================
# GET JOBS BY USER
# ============================================================

def get_jobs_by_user(user_id):

    jobs = list(
        jobs_collection.find({
            "user_id": user_id
        })
    )

    for job in jobs:
        job["_id"] = str(job["_id"])

    return jobs