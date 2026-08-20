from database.db import db
from bson import ObjectId


# ============================================================
# JOBS COLLECTION
# ============================================================

jobs_collection = db["jobs"]


# ============================================================
# CREATE JOB
# ============================================================

def create_job(job_data):

    job_document = {

        "user_id":
            job_data.get("user_id"),

        "title":
            job_data.get("title"),

        "company":
            job_data.get("company"),

        "description":
            job_data.get("description"),

        "required_skills":
            job_data.get(
                "required_skills",
                []
            )
    }

    result = jobs_collection.insert_one(
        job_document
    )

    return str(
        result.inserted_id
    )


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

    if job:

        job["_id"] = str(
            job["_id"]
        )

    return job


# ============================================================
# GET ALL JOBS
# ============================================================

def get_all_jobs():

    jobs = list(
        jobs_collection.find({})
    )

    for job in jobs:

        job["_id"] = str(
            job["_id"]
        )

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

        job["_id"] = str(
            job["_id"]
        )

    return jobs


# ============================================================
# UPDATE JOB
# ============================================================

def update_job(job_id, job_data):

    try:

        update_fields = {}

        if "title" in job_data:
            update_fields["title"] = job_data["title"]

        if "company" in job_data:
            update_fields["company"] = job_data["company"]

        if "description" in job_data:
            update_fields["description"] = job_data["description"]

        if "required_skills" in job_data:
            update_fields["required_skills"] = job_data[
                "required_skills"
            ]

        if not update_fields:
            return False

        result = jobs_collection.update_one(
            {
                "_id": ObjectId(job_id)
            },
            {
                "$set": update_fields
            }
        )

        return result.modified_count > 0 or result.matched_count > 0

    except Exception:

        return False


# ============================================================
# DELETE JOB
# ============================================================

def delete_job(job_id):

    try:

        result = jobs_collection.delete_one({
            "_id": ObjectId(job_id)
        })

        return result.deleted_count > 0

    except Exception:

        return False