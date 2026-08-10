from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.pdf_service import extract_text_from_pdf
from services.resume_parser import parse_resume
from database.resume_repository import save_resume
import os


resume_bp = Blueprint("resume", __name__)


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@resume_bp.route("/resumes/upload", methods=["POST"])
def upload_resume():

    # ---------------------------------------
    # 1. Check whether a file was provided
    # ---------------------------------------

    if "resume" not in request.files:

        return jsonify({
            "error": "No resume file provided"
        }), 400


    file = request.files["resume"]


    # ---------------------------------------
    # 2. Check whether a file was selected
    # ---------------------------------------

    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    # ---------------------------------------
    # 3. Check file type
    # ---------------------------------------

    if not allowed_file(file.filename):

        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400


    # ---------------------------------------
    # 4. Make filename safe
    # ---------------------------------------

    filename = secure_filename(file.filename)


    # ---------------------------------------
    # 5. Create upload folder
    # ---------------------------------------

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


    # ---------------------------------------
    # 6. Create file path
    # ---------------------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    # ---------------------------------------
    # 7. Save PDF
    # ---------------------------------------

    file.save(file_path)


    # ---------------------------------------
    # 8. Extract text
    # ---------------------------------------

    extracted_text = extract_text_from_pdf(
        file_path
    )


    # ---------------------------------------
    # 9. Parse resume
    # ---------------------------------------

    parsed_resume = parse_resume(
        extracted_text
    )


    # ---------------------------------------
    # 10. Save resume to MongoDB
    # ---------------------------------------

    resume_id = save_resume(
        parsed_resume
    )


    # ---------------------------------------
    # 11. Return response
    # ---------------------------------------

    return jsonify({

        "message":
            "Resume uploaded and processed successfully",

        "resume_id":
            resume_id,

        "filename":
            filename,

    }), 201