from flask import Blueprint, request, jsonify
from services.job_service import create_job
from database.job_repository import save_job


job_bp = Blueprint("job", __name__)


@job_bp.route("/jobs", methods=["POST"])
def create_job_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    job_description = data.get("job_description")

    if not job_description:
        return jsonify({
            "error": "Job description is required"
        }), 400

    # Parse job description
    job = create_job(job_description)

    # Save job to MongoDB
    job_id = save_job(job)

    return jsonify({
        "message": "Job created successfully",
        "job_id": job_id,
        "required_skills": job["required_skills"]
    }), 201