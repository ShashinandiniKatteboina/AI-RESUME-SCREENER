from flask import Blueprint, request, jsonify

from services.job_service import process_job_description

from database.job_repository import (
    save_job,
    get_job,
    get_all_jobs,
    get_jobs_by_user
)

from utils.auth import token_required


# ============================================================
# BLUEPRINT
# ============================================================

job_bp = Blueprint("job", __name__)


# ============================================================
# CREATE JOB
# ============================================================

@job_bp.route("/jobs", methods=["POST"])
@token_required
def create_job():

    # --------------------------------------------------------
    # Get request data
    # --------------------------------------------------------

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    # --------------------------------------------------------
    # Get fields
    # --------------------------------------------------------

    title = data.get("title")
    company = data.get("company")
    description = data.get("description")

    # --------------------------------------------------------
    # Validate title
    # --------------------------------------------------------

    if not title:
        return jsonify({
            "error": "title is required"
        }), 400

    # --------------------------------------------------------
    # Validate description
    # --------------------------------------------------------

    if not description:
        return jsonify({
            "error": "description is required"
        }), 400

    # --------------------------------------------------------
    # Extract required skills
    # --------------------------------------------------------

    required_skills = process_job_description(
        description
    )

    if not isinstance(required_skills, list):
        return jsonify({
            "error": "required_skills must be an array"
        }), 400

    # --------------------------------------------------------
    # Create job document
    # --------------------------------------------------------

    job_data = {
        "user_id": request.user_id,
        "title": title,
        "company": company,
        "description": description,
        "required_skills": required_skills
    }

    # --------------------------------------------------------
    # Save job
    # --------------------------------------------------------

    job_id = save_job(job_data)

    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return jsonify({

        "message": "Job created successfully",

        "job_id": job_id,

        "user_id": request.user_id,

        "job": {
            "title": title,
            "company": company,
            "description": description,
            "required_skills": required_skills
        }

    }), 201


# ============================================================
# GET MY JOBS
# ============================================================

@job_bp.route("/jobs", methods=["GET"])
@token_required
def get_jobs():

    jobs = get_jobs_by_user(
        request.user_id
    )

    return jsonify({

        "user_id": request.user_id,

        "total_jobs": len(jobs),

        "jobs": jobs

    }), 200


# ============================================================
# GET ONE JOB
# ============================================================

@job_bp.route("/jobs/<job_id>", methods=["GET"])
@token_required
def get_single_job(job_id):

    job = get_job(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    # --------------------------------------------------------
    # Ownership check
    # --------------------------------------------------------

    if job.get("user_id") != request.user_id:

        return jsonify({
            "error": "You are not authorized to access this job"
        }), 403

    return jsonify({

        "message": "Job retrieved successfully",

        "job": job

    }), 200