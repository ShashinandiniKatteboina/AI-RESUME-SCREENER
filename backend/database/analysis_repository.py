
from database.db import db

from bson import ObjectId


# ============================================================
# ANALYSES COLLECTION
# ============================================================

analyses_collection = db["analyses"]


# ============================================================
# CREATE ANALYSIS
# ============================================================

def create_analysis(analysis_data):

    result = analyses_collection.insert_one(
        analysis_data
    )

    return str(
        result.inserted_id
    )


# ============================================================
# GET ONE ANALYSIS
# ============================================================

def get_analysis(analysis_id):

    try:

        analysis = analyses_collection.find_one({
            "_id": ObjectId(analysis_id)
        })

    except Exception:

        return None

    if not analysis:

        return None

    analysis["_id"] = str(
        analysis["_id"]
    )

    return analysis


# ============================================================
# GET ALL ANALYSES
# ============================================================

def get_all_analyses():

    analyses = list(
        analyses_collection.find({})
    )

    for analysis in analyses:

        analysis["_id"] = str(
            analysis["_id"]
        )

    return analyses


# ============================================================
# GET ANALYSES BY USER
# ============================================================

def get_analyses_by_user(user_id):

    analyses = list(
        analyses_collection.find({
            "user_id": user_id
        })
    )

    for analysis in analyses:

        analysis["_id"] = str(
            analysis["_id"]
        )

    return analyses


# ============================================================
# GET ANALYSES BY RESUME
# ============================================================

def get_analyses_by_resume(resume_id):

    analyses = list(
        analyses_collection.find({
            "resume_id": resume_id
        })
    )

    for analysis in analyses:

        analysis["_id"] = str(
            analysis["_id"]
        )

    return analyses


# ============================================================
# GET ANALYSES BY JOB
# ============================================================

def get_analyses_by_job(job_id):

    analyses = list(
        analyses_collection.find({
            "job_id": job_id
        })
    )

    for analysis in analyses:

        analysis["_id"] = str(
            analysis["_id"]
        )

    return analyses


# ============================================================
# DELETE ANALYSIS
# ============================================================

def delete_analysis(analysis_id):

    try:

        result = analyses_collection.delete_one({
            "_id": ObjectId(analysis_id)
        })

        return result.deleted_count > 0

    except Exception:

        return False
