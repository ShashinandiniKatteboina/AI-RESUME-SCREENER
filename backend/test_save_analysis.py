from database.resume_repository import get_resume
from database.analysis_repository import save_analysis
from services.analysis_service import analyze_resume


# Resume stored in MongoDB
resume_id = "6a780c4278f66ba576a9084a"


# Get resume
resume = get_resume(resume_id)


if not resume:

    print("❌ Resume not found")

    exit()


print("✅ Resume retrieved")


# Job description
job_description = """
Software Engineer

Requirements:
Java
Python
SQL
Node JS
MongoDB
Git
React
RESTful APIs
Data Structures
"""


# Analyze resume
analysis = analyze_resume(
    resume,
    job_description
)


# Add resume ID
analysis["resume_id"] = resume_id


# Save analysis
analysis_id = save_analysis(analysis)


print("\n===== ANALYSIS SAVED =====")

print("Analysis ID:", analysis_id)

print("Match Score:",
      analysis["match_score"], "%")

print("Matched Skills:",
      analysis["matched_skills"])

print("Missing Skills:",
      analysis["missing_skills"])