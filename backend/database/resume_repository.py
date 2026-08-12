from database.db import db
from bson import ObjectId


# ============================================================
# SAVE RESUME
# ============================================================

def save_resume(resume_data):

    collection = db["resumes"]

    result = collection.insert_one(resume_data)

    return str(result.inserted_id)


# ============================================================
# GET ONE RESUME
# ============================================================

def get_resume(resume_id):

    collection = db["resumes"]

    resume = collection.find_one({
        "_id": ObjectId(resume_id)
    })

    if resume:
        resume["_id"] = str(resume["_id"])

    return resume


# ============================================================
# GET ALL RESUMES
# ============================================================

def get_all_resumes():

    collection = db["resumes"]

    resumes = collection.find()

    result = []

    for resume in resumes:

        resume["_id"] = str(resume["_id"])

        result.append(resume)

    return result


# ============================================================
# GET RESUMES BY USER
# ============================================================

def get_resumes_by_user(user_id):

    collection = db["resumes"]

    resumes = collection.find({
        "user_id": user_id
    })

    result = []

    for resume in resumes:

        resume["_id"] = str(resume["_id"])

        result.append(resume)

    return result