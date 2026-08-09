from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
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

    if "resume" not in request.files:
        return jsonify({
            "error": "No resume file provided"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400

    filename = secure_filename(file.filename)

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(file_path)

    return jsonify({
        "message": "Resume uploaded successfully",
        "filename": filename
    }), 201