from flask import Blueprint, request, jsonify

from database.resume_repository import get_resume
from database.job_repository import get_job

from database.analysis_repository import (
    save_analysis,
    get_analysis,
    get_analyses_by_resume
)

from services.analysis_service import analyze_resume
from services.ai_service import generate_ai_analysis


# ============================================================
# BLUEPRINT
# ============================================================

analysis_bp = Blueprint("analysis", __name__)


# ============================================================
# CREATE ANALYSIS
# ============================================================

@analysis_bp.route("/analysis", methods=["POST"])
def create_analysis():

    # --------------------------------------------------------
    # Get request data
    # --------------------------------------------------------

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    resume_id = data.get("resume_id")
    job_id = data.get("job_id")

    # --------------------------------------------------------
    # Validate resume ID
    # --------------------------------------------------------

    if not resume_id:
        return jsonify({
            "error": "resume_id is required"
        }), 400

    # --------------------------------------------------------
    # Validate job ID
    # --------------------------------------------------------

    if not job_id:
        return jsonify({
            "error": "job_id is required"
        }), 400

    # --------------------------------------------------------
    # Get resume from MongoDB
    # --------------------------------------------------------

    resume = get_resume(resume_id)

    if not resume:
        return jsonify({
            "error": "Resume not found"
        }), 404

    # --------------------------------------------------------
    # Get job from MongoDB
    # --------------------------------------------------------

    job = get_job(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    # --------------------------------------------------------
    # Check required skills
    # --------------------------------------------------------

    required_skills = job.get("required_skills", [])

    if not required_skills:
        return jsonify({
            "error": "Job has no required skills"
        }), 400

    # --------------------------------------------------------
    # Perform resume-job matching
    # --------------------------------------------------------

    analysis = analyze_resume(
        resume,
        job["description"],
        required_skills
    )

    # --------------------------------------------------------
    # Generate Gemini AI analysis
    # --------------------------------------------------------

    ai_analysis = generate_ai_analysis(
        resume=resume,
        job_description=job["description"],
        match_score=analysis["match_score"],
        matched_skills=analysis["matched_skills"],
        missing_skills=analysis["missing_skills"]
    )

    # --------------------------------------------------------
    # Add AI analysis
    # --------------------------------------------------------

    analysis["ai_analysis"] = ai_analysis

    # --------------------------------------------------------
    # Add IDs
    # --------------------------------------------------------

    analysis["resume_id"] = resume_id
    analysis["job_id"] = job_id

    # --------------------------------------------------------
    # Save analysis to MongoDB
    # --------------------------------------------------------

    analysis_id = save_analysis(analysis)

    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return jsonify({

        "message": "Analysis completed successfully",

        "analysis_id": analysis_id,

        "resume_id": resume_id,

        "job_id": job_id,

        "match_score": analysis["match_score"],

        "matched_skills": analysis["matched_skills"],

        "missing_skills": analysis["missing_skills"],

        "skill_gap": analysis.get(
            "skill_gap",
            {}
        ),

        "ai_analysis": analysis["ai_analysis"]

    }), 201


# ============================================================
# GET ALL ANALYSES FOR A RESUME
# ============================================================

@analysis_bp.route(
    "/analysis/resume/<resume_id>",
    methods=["GET"]
)
def get_resume_analysis_history(resume_id):

    analyses = get_analyses_by_resume(resume_id)

    return jsonify({

        "resume_id": resume_id,

        "total_analyses": len(analyses),

        "analyses": analyses

    }), 200


# ============================================================
# GET ONE ANALYSIS
# ============================================================

@analysis_bp.route(
    "/analysis/<analysis_id>",
    methods=["GET"]
)
def get_single_analysis(analysis_id):

    analysis = get_analysis(analysis_id)

    if not analysis:
        return jsonify({
            "error": "Analysis not found"
        }), 404

    return jsonify({

        "message": "Analysis retrieved successfully",

        "analysis": analysis

    }), 200