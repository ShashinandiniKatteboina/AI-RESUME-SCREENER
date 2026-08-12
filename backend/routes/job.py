
from flask import Blueprint, request, jsonify

from database.job_repository import (
    create_job,
    get_job,
    get_all_jobs,
    get_jobs_by_user,
    update_job,
    delete_job
)

from utils.auth import token_required


# ============================================================
# BLUEPRINT
# ============================================================

job_bp = Blueprint(
    "job",
    __name__
)


# ============================================================
# CREATE JOB
# ============================================================

@job_bp.route(
    "/jobs",
    methods=["POST"]
)
@token_required
def create_job_route():

    # --------------------------------------------------------
    # Get logged-in user
    # --------------------------------------------------------

    user_id = request.user_id

    # --------------------------------------------------------
    # Get request body
    # --------------------------------------------------------

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    # --------------------------------------------------------
    # Get job details
    # --------------------------------------------------------

    title = data.get("title")
    description = data.get("description")
    required_skills = data.get(
        "required_skills",
        []
    )

    # --------------------------------------------------------
    # Validate title
    # --------------------------------------------------------

    if not title:

        return jsonify({
            "error": "Job title is required"
        }), 400

    # --------------------------------------------------------
    # Validate skills
    # --------------------------------------------------------

    if not isinstance(
        required_skills,
        list
    ):

        return jsonify({
            "error": "required_skills must be a list"
        }), 400

    # --------------------------------------------------------
    # Create job document
    # --------------------------------------------------------

    job_data = {

        "user_id": user_id,

        "title": title,

        "description": description,

        "required_skills": required_skills
    }

    # --------------------------------------------------------
    # Save job
    # --------------------------------------------------------

    job_id = create_job(
        job_data
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return jsonify({

        "message":
            "Job created successfully",

        "job_id":
            job_id,

        "user_id":
            user_id,

        "title":
            title,

        "description":
            description,

        "required_skills":
            required_skills

    }), 201


# ============================================================
# GET ALL JOBS
# ============================================================

@job_bp.route(
    "/jobs",
    methods=["GET"]
)
@token_required
def get_jobs():

    jobs = get_all_jobs()

    return jsonify({

        "total_jobs":
            len(jobs),

        "jobs":
            jobs

    }), 200


# ============================================================
# GET MY JOBS
# ============================================================

@job_bp.route(
    "/jobs/my",
    methods=["GET"]
)
@token_required
def get_my_jobs():

    user_id = request.user_id

    jobs = get_jobs_by_user(
        user_id
    )

    return jsonify({

        "user_id":
            user_id,

        "total_jobs":
            len(jobs),

        "jobs":
            jobs

    }), 200


# ============================================================
# GET ONE JOB
# ============================================================

@job_bp.route(
    "/jobs/<job_id>",
    methods=["GET"]
)
@token_required
def get_single_job(job_id):

    user_id = request.user_id

    job = get_job(
        job_id
    )

    if not job:

        return jsonify({
            "error": "Job not found"
        }), 404

    # --------------------------------------------------------
    # Ownership check
    # --------------------------------------------------------

    if job.get("user_id") != user_id:

        return jsonify({
            "error":
                "You are not authorized to access this job"
        }), 403

    return jsonify({

        "message":
            "Job retrieved successfully",

        "job":
            job

    }), 200


# ============================================================
# UPDATE JOB
# ============================================================

@job_bp.route(
    "/jobs/<job_id>",
    methods=["PUT"]
)
@token_required
def update_job_route(job_id):

    user_id = request.user_id

    # --------------------------------------------------------
    # Find job
    # --------------------------------------------------------

    job = get_job(
        job_id
    )

    if not job:

        return jsonify({
            "error": "Job not found"
        }), 404

    # --------------------------------------------------------
    # Ownership check
    # --------------------------------------------------------

    if job.get("user_id") != user_id:

        return jsonify({
            "error":
                "You are not authorized to update this job"
        }), 403

    # --------------------------------------------------------
    # Get request body
    # --------------------------------------------------------

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    # --------------------------------------------------------
    # Only allow these fields to be updated
    # --------------------------------------------------------

    update_data = {}

    if "title" in data:

        update_data["title"] = data["title"]

    if "description" in data:

        update_data["description"] = data["description"]

    if "required_skills" in data:

        if not isinstance(
            data["required_skills"],
            list
        ):

            return jsonify({
                "error":
                    "required_skills must be a list"
            }), 400

        update_data["required_skills"] = (
            data["required_skills"]
        )

    # --------------------------------------------------------
    # Check whether anything was provided
    # --------------------------------------------------------

    if not update_data:

        return jsonify({
            "error":
                "No valid fields provided for update"
        }), 400

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    updated = update_job(
        job_id,
        update_data
    )

    # --------------------------------------------------------
    # Return updated job
    # --------------------------------------------------------

    updated_job = get_job(
        job_id
    )

    return jsonify({

        "message":
            "Job updated successfully",

        "job":
            updated_job

    }), 200


# ============================================================
# DELETE JOB
# ============================================================

@job_bp.route(
    "/jobs/<job_id>",
    methods=["DELETE"]
)
@token_required
def delete_job_route(job_id):

    user_id = request.user_id

    # --------------------------------------------------------
    # Find job
    # --------------------------------------------------------

    job = get_job(
        job_id
    )

    if not job:

        return jsonify({
            "error": "Job not found"
        }), 404

    # --------------------------------------------------------
    # Ownership check
    # --------------------------------------------------------

    if job.get("user_id") != user_id:

        return jsonify({
            "error":
                "You are not authorized to delete this job"
        }), 403

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

    deleted = delete_job(
        job_id
    )

    if not deleted:

        return jsonify({
            "error":
                "Failed to delete job"
        }), 500

    return jsonify({

        "message":
            "Job deleted successfully",

        "job_id":
            job_id

    }), 200
