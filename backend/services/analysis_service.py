from services.job_service import create_job
from services.matching_service import generate_match_result


def analyze_resume(resume, job_description):

    # Parse job description
    job = create_job(job_description)

    # Match resume with job
    result = generate_match_result(
        resume,
        job["required_skills"]
    )

    return {
        "job_description": job_description,
        "required_skills": job["required_skills"],
        "match_score": result["match_score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "total_required_skills": result["total_required_skills"],
        "total_matched_skills": result["total_matched_skills"],
        "total_missing_skills": result["total_missing_skills"]
    }