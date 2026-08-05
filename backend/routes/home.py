from flask import Blueprint, jsonify

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return "AI Resume Screening Platform"

@home_bp.route("/about")
def about():
    return jsonify({
        "project": "AI Resume Screening Platform",
        "version": "1.0",
        "developer": "Shashi"
    })

@home_bp.route("/health")
def health():
    return jsonify({
        "status": "Running",
        "message": "Backend is working successfully"
    })