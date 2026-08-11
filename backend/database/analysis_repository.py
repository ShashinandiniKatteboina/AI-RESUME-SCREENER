from database.db import db
from bson import ObjectId


# ============================================================
# SAVE ANALYSIS
# ============================================================

def save_analysis(analysis_data):

    collection = db["analyses"]

    result = collection.insert_one(analysis_data)

    return str(result.inserted_id)


# ============================================================
# GET ONE ANALYSIS
# ============================================================

def get_analysis(analysis_id):

    collection = db["analyses"]

    analysis = collection.find_one({
        "_id": ObjectId(analysis_id)
    })

    if analysis:
        analysis["_id"] = str(analysis["_id"])

    return analysis


# ============================================================
# GET ALL ANALYSES FOR A RESUME
# ============================================================

def get_analyses_by_resume(resume_id):

    collection = db["analyses"]

    analyses = collection.find({
        "resume_id": resume_id
    })

    result = []

    for analysis in analyses:

        analysis["_id"] = str(analysis["_id"])

        result.append(analysis)

    return result