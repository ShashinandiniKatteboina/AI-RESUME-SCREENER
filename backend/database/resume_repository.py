from database.db import db
from bson import ObjectId


# ============================================================
# RESUMES COLLECTION
# ============================================================

resumes_collection = db["resumes"]


# ============================================================
# SAVE RESUME
# ============================================================

def save_resume(resume_data):

    resume_document = {

        "user_id":
            resume_data.get("user_id"),

        "filename":
            resume_data.get("filename"),

        "text":
            resume_data.get("text"),

        "parsed_resume":
            resume_data.get(
                "parsed_resume",
                {}
            )
    }

    result = resumes_collection.insert_one(
        resume_document
    )

    return str(
        result.inserted_id
    )


# ============================================================
# GET ONE RESUME
# ============================================================

def get_resume(resume_id):

    try:

        resume = resumes_collection.find_one({
            "_id": ObjectId(resume_id)
        })

    except Exception:

        return None

    if resume:

        resume["_id"] = str(
            resume["_id"]
        )

    return resume


# ============================================================
# GET RESUMES BY USER
# ============================================================

def get_resumes_by_user(user_id):

    resumes = list(
        resumes_collection.find({
            "user_id": user_id
        })
    )

    for resume in resumes:

        resume["_id"] = str(
            resume["_id"]
        )

    return resumes


# ============================================================
# DELETE RESUME
# ============================================================

def delete_resume(resume_id):

    try:

        result = resumes_collection.delete_one({
            "_id": ObjectId(resume_id)
        })

        return result.deleted_count > 0

    except Exception:

        return False