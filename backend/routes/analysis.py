from flask import Blueprint, request, jsonify

from database.analysis_repository import (
    create_analysis,
    get_analysis,
    get_analyses_by_user
)

from database.resume_repository import (
    get_resume
)

from database.job_repository import (
    get_job
)

from services.matching_service import (
    generate_match_result
)

from services.ai_service import (
    generate_ai_analysis
)

from utils.auth import token_required


# ============================================================
# BLUEPRINT
# ============================================================

analysis_bp = Blueprint(
    "analysis",
    __name__
)


# ============================================================
# CREATE ANALYSIS
# ============================================================

@analysis_bp.route(
    "/analysis",
    methods=["POST"]
)
@token_required
def analyze_resume():

    # --------------------------------------------------------
    # Get logged-in user
    # --------------------------------------------------------

    user_id = request.user_id

    # --------------------------------------------------------
    # Get request data
    # --------------------------------------------------------

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    # --------------------------------------------------------
    # Get resume ID
    # --------------------------------------------------------

    resume_id = data.get("resume_id")

    if not resume_id:

        return jsonify({
            "error": "resume_id is required"
        }), 400

    # --------------------------------------------------------
    # Get job ID
    # --------------------------------------------------------

    job_id = data.get("job_id")

    if not job_id:

        return jsonify({
            "error": "job_id is required"
        }), 400

    # --------------------------------------------------------
    # Get resume
    # --------------------------------------------------------

    resume = get_resume(
        resume_id
    )

    if not resume:

        return jsonify({
            "error": "Resume not found"
        }), 404

    # --------------------------------------------------------
    # Check resume ownership
    # --------------------------------------------------------

    if resume.get("user_id") != user_id:

        return jsonify({
            "error":
                "You are not authorized to analyze this resume"
        }), 403

    # --------------------------------------------------------
    # Get job
    # --------------------------------------------------------

    job = get_job(
        job_id
    )

    if not job:

        return jsonify({
            "error": "Job not found"
        }), 404

    # --------------------------------------------------------
    # Get required skills
    # --------------------------------------------------------

    job_skills = job.get(
        "required_skills",
        []
    )

    # --------------------------------------------------------
    # Generate rule-based matching result
    # --------------------------------------------------------

    match_result = generate_match_result(
        resume,
        job_skills
    )

    # --------------------------------------------------------
    # Generate AI analysis
    # --------------------------------------------------------

    ai_analysis = generate_ai_analysis(
        resume,
        job,
        match_result.get(
            "match_score",
            0
        ),
        match_result.get(
            "matched_skills",
            []
        ),
        match_result.get(
            "missing_skills",
            []
        )
    )

    # --------------------------------------------------------
    # Create analysis document
    # --------------------------------------------------------

    analysis_data = {

        "user_id":
            user_id,

        "resume_id":
            resume_id,

        "job_id":
            job_id,

        "job_description":
            job.get(
                "description",
                ""
            ),

        "required_skills":
            job_skills,

        "match_score":
            match_result.get(
                "match_score",
                0
            ),

        "matched_skills":
            match_result.get(
                "matched_skills",
                []
            ),

        "missing_skills":
            match_result.get(
                "missing_skills",
                []
            ),

        "skill_gap":
            match_result.get(
                "skill_gap",
                {}
            ),

        "total_required_skills":
            match_result.get(
                "total_required_skills",
                0
            ),

        "total_matched_skills":
            match_result.get(
                "total_matched_skills",
                0
            ),

        "total_missing_skills":
            match_result.get(
                "total_missing_skills",
                0
            ),

        "ai_analysis":
            ai_analysis
    }

    # --------------------------------------------------------
    # Save analysis
    # --------------------------------------------------------

    analysis_id = create_analysis(
        analysis_data
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return jsonify({

        "message":
            "Analysis completed successfully",

        "analysis_id":
            analysis_id,

        "resume_id":
            resume_id,

        "job_id":
            job_id,

        "match_score":
            match_result.get(
                "match_score",
                0
            ),

        "matched_skills":
            match_result.get(
                "matched_skills",
                []
            ),

        "missing_skills":
            match_result.get(
                "missing_skills",
                []
            ),

        "skill_gap":
            match_result.get(
                "skill_gap",
                {}
            ),

        "ai_analysis":
            ai_analysis

    }), 201


# ============================================================
# GET MY ANALYSES
# ============================================================

@analysis_bp.route(
    "/analysis/my",
    methods=["GET"]
)
@token_required
def get_my_analyses():

    # --------------------------------------------------------
    # Get logged-in user's ID
    # --------------------------------------------------------

    user_id = request.user_id

    # --------------------------------------------------------
    # Get user's analyses
    # --------------------------------------------------------

    analyses = get_analyses_by_user(
        user_id
    )

    # --------------------------------------------------------
    # Return analyses
    # --------------------------------------------------------

    return jsonify({

        "user_id":
            user_id,

        "total_analyses":
            len(analyses),

        "analyses":
            analyses

    }), 200


# ============================================================
# GET ONE ANALYSIS
# ============================================================

@analysis_bp.route(
    "/analysis/<analysis_id>",
    methods=["GET"]
)
@token_required
def get_single_analysis(
    analysis_id
):

    # --------------------------------------------------------
    # Get logged-in user's ID
    # --------------------------------------------------------

    user_id = request.user_id

    # --------------------------------------------------------
    # Get analysis
    # --------------------------------------------------------

    analysis = get_analysis(
        analysis_id
    )

    if not analysis:

        return jsonify({
            "error": "Analysis not found"
        }), 404

    # --------------------------------------------------------
    # Check ownership
    # --------------------------------------------------------

    if analysis.get("user_id") != user_id:

        return jsonify({
            "error":
                "You are not authorized to access this analysis"
        }), 403

    # --------------------------------------------------------
    # Return analysis
    # --------------------------------------------------------

    return jsonify({

        "message":
            "Analysis retrieved successfully",

        "analysis":
            analysis

    }), 200