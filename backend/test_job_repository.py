from database.job_repository import save_job, get_job, get_all_jobs


# ============================================================
# CREATE TEST JOB
# ============================================================

job_data = {
    "title": "Software Engineer",
    "company": "Test Company",
    "description": """
    Software Engineer

    Requirements:
    Java
    Python
    SQL
    MongoDB
    Git
    React
    Data Structures
    """,
    "required_skills": [
        "Java",
        "Python",
        "SQL",
        "MongoDB",
        "Git",
        "React",
        "Data Structures"
    ]
}


# ============================================================
# SAVE JOB
# ============================================================

job_id = save_job(job_data)

print("✅ Job saved successfully")

print("Job ID:")
print(job_id)


# ============================================================
# GET JOB
# ============================================================

job = get_job(job_id)

print("\n===== RETRIEVED JOB =====")

print(job)


# ============================================================
# GET ALL JOBS
# ============================================================

jobs = get_all_jobs()

print("\n===== ALL JOBS =====")

print("Total jobs:", len(jobs))

for item in jobs:

    print("\nJob ID:", item["_id"])
    print("Title:", item.get("title"))
    print("Company:", item.get("company"))