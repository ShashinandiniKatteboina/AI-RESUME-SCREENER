from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.pdf_service import extract_text_from_pdf
import os


resume_bp = Blueprint("resume", __name__)

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@resume_bp.route("/resumes/upload", methods=["POST"])
def upload_resume():

    # Check whether a file was provided
    if "resume" not in request.files:
        return jsonify({
            "error": "No resume file provided"
        }), 400

    file = request.files["resume"]

    # Check whether a file was selected
    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    # Check file type
    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400

    # Make filename safe
    filename = secure_filename(file.filename)

    # Create file path
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save PDF
    file.save(file_path)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    return jsonify({
        "message": "Resume uploaded and processed successfully",
        "filename": filename,
        "text": extracted_text
    }), 201