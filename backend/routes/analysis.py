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

from utils.auth import token_required


# ============================================================
# BLUEPRINT
# ============================================================

analysis_bp = Blueprint("analysis", __name__)


# ============================================================
# CREATE ANALYSIS
# ============================================================

@analysis_bp.route("/analysis", methods=["POST"])
@token_required
def create_analysis():

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
    # Get resume
    # --------------------------------------------------------

    resume = get_resume(resume_id)

    if not resume:
        return jsonify({
            "error": "Resume not found"
        }), 404

    # --------------------------------------------------------
    # Check resume ownership
    # --------------------------------------------------------

    if resume.get("user_id") != request.user_id:

        return jsonify({
            "error": "You are not authorized to analyze this resume"
        }), 403

    # --------------------------------------------------------
    # Get job
    # --------------------------------------------------------

    job = get_job(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    # --------------------------------------------------------
    # Perform matching
    # --------------------------------------------------------

    analysis = analyze_resume(
        resume,
        job["description"],
        job["required_skills"]
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
    analysis["user_id"] = request.user_id

    # --------------------------------------------------------
    # Save analysis
    # --------------------------------------------------------

    analysis_id = save_analysis(analysis)

    # --------------------------------------------------------
    # Response
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
# GET MY ANALYSIS HISTORY
# ============================================================

@analysis_bp.route(
    "/analysis/resume/<resume_id>",
    methods=["GET"]
)
@token_required
def get_resume_analysis_history(resume_id):

    # --------------------------------------------------------
    # Check resume exists
    # --------------------------------------------------------

    resume = get_resume(resume_id)

    if not resume:
        return jsonify({
            "error": "Resume not found"
        }), 404

    # --------------------------------------------------------
    # Check ownership
    # --------------------------------------------------------

    if resume.get("user_id") != request.user_id:

        return jsonify({
            "error": "You are not authorized to access this resume"
        }), 403

    # --------------------------------------------------------
    # Get analyses
    # --------------------------------------------------------

    analyses = get_analyses_by_resume(resume_id)

    return jsonify({

        "user_id": request.user_id,

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
@token_required
def get_single_analysis(analysis_id):

    # --------------------------------------------------------
    # Get analysis
    # --------------------------------------------------------

    analysis = get_analysis(analysis_id)

    if not analysis:
        return jsonify({
            "error": "Analysis not found"
        }), 404

    # --------------------------------------------------------
    # Check ownership
    # --------------------------------------------------------

    if analysis.get("user_id") != request.user_id:

        return jsonify({
            "error": "You are not authorized to access this analysis"
        }), 403

    # --------------------------------------------------------
    # Return analysis
    # --------------------------------------------------------

    return jsonify({

        "message": "Analysis retrieved successfully",

        "analysis": analysis

    }), 200