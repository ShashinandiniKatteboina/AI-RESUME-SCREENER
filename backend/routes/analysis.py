from flask import Blueprint, request, jsonify

from database.resume_repository import get_resume
from database.job_repository import get_job
from database.analysis_repository import save_analysis

from services.analysis_service import analyze_resume


analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/analysis", methods=["POST"])
def create_analysis():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    resume_id = data.get("resume_id")
    job_id = data.get("job_id")

    if not resume_id:
        return jsonify({
            "error": "resume_id is required"
        }), 400

    if not job_id:
        return jsonify({
            "error": "job_id is required"
        }), 400

    # Get resume
    resume = get_resume(resume_id)

    if not resume:
        return jsonify({
            "error": "Resume not found"
        }), 404

    # Get job
    job = get_job(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    # Analyze
    analysis = analyze_resume(
        resume,
        job["description"]
    )

    # Add IDs
    analysis["resume_id"] = resume_id
    analysis["job_id"] = job_id

    # Save analysis
    analysis_id = save_analysis(analysis)

    return jsonify({
        "message": "Analysis completed successfully",
        "analysis_id": analysis_id,
        "resume_id": resume_id,
        "job_id": job_id,
        "match_score": analysis["match_score"],
        "matched_skills": analysis["matched_skills"],
        "missing_skills": analysis["missing_skills"]
    }), 201