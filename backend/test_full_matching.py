from database.resume_repository import get_resume
from services.job_service import create_job
from services.matching_service import generate_match_result


# ==========================================
# 1. GET RESUME FROM MONGODB
# ==========================================

resume_id = "6a780c4278f66ba576a9084a"

resume = get_resume(resume_id)


if not resume:

    print("❌ Resume not found")

    exit()


print("✅ Resume retrieved from MongoDB")


# ==========================================
# 2. REAL JOB DESCRIPTION
# ==========================================

job_description = """
Software Engineer

We are looking for a Software Engineer with
strong programming and problem-solving skills.

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


# ==========================================
# 3. PARSE JOB DESCRIPTION
# ==========================================

job = create_job(job_description)


print("\n===== JOB SKILLS =====")

for skill in job["required_skills"]:
    print(skill)


# ==========================================
# 4. MATCH RESUME WITH JOB
# ==========================================

result = generate_match_result(
    resume,
    job["required_skills"]
)


# ==========================================
# 5. DISPLAY RESULT
# ==========================================

print("\n===== FINAL MATCHING RESULT =====")

print(
    "Match Score:",
    result["match_score"],
    "%"
)


print("\nMatched Skills:")

for skill in result["matched_skills"]:
    print("✅", skill)


print("\nMissing Skills:")

for skill in result["missing_skills"]:
    print("❌", skill)


print(
    "\nTotal Required Skills:",
    result["total_required_skills"]
)

print(
    "Total Matched Skills:",
    result["total_matched_skills"]
)

print(
    "Total Missing Skills:",
    result["total_missing_skills"]
)