
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from services.pdf_service import extract_text_from_pdf

from database.resume_repository import (
    save_resume,
    get_resume,
    get_resumes_by_user,
    delete_resume
)

from utils.auth import token_required

import os


# ============================================================
# BLUEPRINT
# ============================================================

resume_bp = Blueprint("resume", __name__)


# ============================================================
# UPLOAD FOLDER
# ============================================================

UPLOAD_FOLDER = "uploads"


# ============================================================
# ALLOWED EXTENSIONS
# ============================================================

ALLOWED_EXTENSIONS = {"pdf"}


# ============================================================
# CHECK FILE EXTENSION
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# UPLOAD RESUME
# ============================================================

@resume_bp.route("/resumes/upload", methods=["POST"])
@token_required
def upload_resume():

    # --------------------------------------------------------
    # Get logged-in user's ID from JWT
    # --------------------------------------------------------

    user_id = request.user_id


    # --------------------------------------------------------
    # Check whether file was provided
    # --------------------------------------------------------

    if "resume" not in request.files:

        return jsonify({
            "error": "No resume file provided"
        }), 400


    file = request.files["resume"]


    # --------------------------------------------------------
    # Check whether file was selected
    # --------------------------------------------------------

    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    if not allowed_file(file.filename):

        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400


    # --------------------------------------------------------
    # Make filename safe
    # --------------------------------------------------------

    filename = secure_filename(
        file.filename
    )


    # --------------------------------------------------------
    # Create upload folder
    # --------------------------------------------------------

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Create file path
    # --------------------------------------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    # --------------------------------------------------------
    # Save PDF
    # --------------------------------------------------------

    file.save(
        file_path
    )


    # --------------------------------------------------------
    # Extract text from PDF
    # --------------------------------------------------------

    try:

        extracted_text = extract_text_from_pdf(
            file_path
        )

    except Exception as e:

        return jsonify({
            "error": "Failed to extract text from PDF",
            "details": str(e)
        }), 500


    # --------------------------------------------------------
    # Create resume document
    # --------------------------------------------------------

    resume_data = {

        "user_id": user_id,

        "filename": filename,

        "text": extracted_text
    }


    # --------------------------------------------------------
    # Save resume to MongoDB
    # --------------------------------------------------------

    try:

        resume_id = save_resume(
            resume_data
        )

    except Exception as e:

        return jsonify({
            "error": "Failed to save resume",
            "details": str(e)
        }), 500


    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return jsonify({

        "message":
            "Resume uploaded and processed successfully",

        "resume_id":
            resume_id,

        "user_id":
            user_id,

        "filename":
            filename,

        "text":
            extracted_text

    }), 201


# ============================================================
# GET MY RESUMES
# ============================================================

@resume_bp.route("/resumes/my", methods=["GET"])
@token_required
def get_my_resumes():

    # --------------------------------------------------------
    # Get logged-in user's ID from JWT
    # --------------------------------------------------------

    user_id = request.user_id


    # --------------------------------------------------------
    # Get resumes belonging to this user
    # --------------------------------------------------------

    resumes = get_resumes_by_user(
        user_id
    )


    # --------------------------------------------------------
    # Return resumes
    # --------------------------------------------------------

    return jsonify({

        "user_id":
            user_id,

        "total_resumes":
            len(resumes),

        "resumes":
            resumes

    }), 200


# ============================================================
# GET ONE RESUME
# ============================================================

@resume_bp.route("/resumes/<resume_id>", methods=["GET"])
@token_required
def get_single_resume(resume_id):

    # --------------------------------------------------------
    # Get logged-in user's ID from JWT
    # --------------------------------------------------------

    user_id = request.user_id


    # --------------------------------------------------------
    # Get resume
    # --------------------------------------------------------

    resume = get_resume(
        resume_id
    )


    # --------------------------------------------------------
    # Resume not found
    # --------------------------------------------------------

    if not resume:

        return jsonify({
            "error": "Resume not found"
        }), 404


    # --------------------------------------------------------
    # Check ownership
    # --------------------------------------------------------

    if resume.get("user_id") != user_id:

        return jsonify({
            "error":
                "You are not authorized to access this resume"
        }), 403


    # --------------------------------------------------------
    # Return resume
    # --------------------------------------------------------

    return jsonify({

        "message":
            "Resume retrieved successfully",

        "resume":
            resume

    }), 200


# ============================================================
# DELETE RESUME
# ============================================================

@resume_bp.route("/resumes/<resume_id>", methods=["DELETE"])
@token_required
def delete_single_resume(resume_id):

    # --------------------------------------------------------
    # Get logged-in user's ID
    # --------------------------------------------------------

    user_id = request.user_id


    # --------------------------------------------------------
    # Find resume
    # --------------------------------------------------------

    resume = get_resume(
        resume_id
    )


    # --------------------------------------------------------
    # Resume not found
    # --------------------------------------------------------

    if not resume:

        return jsonify({
            "error": "Resume not found"
        }), 404


    # --------------------------------------------------------
    # Check ownership
    # --------------------------------------------------------

    if resume.get("user_id") != user_id:

        return jsonify({
            "error":
                "You are not authorized to delete this resume"
        }), 403


    # --------------------------------------------------------
    # Delete resume from MongoDB
    # --------------------------------------------------------

    deleted = delete_resume(
        resume_id
    )


    # --------------------------------------------------------
    # Check deletion result
    # --------------------------------------------------------

    if not deleted:

        return jsonify({
            "error":
                "Failed to delete resume"
        }), 500


    # --------------------------------------------------------
    # Delete physical PDF file
    # --------------------------------------------------------

    filename = resume.get(
        "filename"
    )

    if filename:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if os.path.exists(file_path):

            try:

                os.remove(
                    file_path
                )

            except Exception:

                pass


    # --------------------------------------------------------
    # Return success
    # --------------------------------------------------------

    return jsonify({

        "message":
            "Resume deleted successfully",

        "resume_id":
            resume_id

    }), 200
