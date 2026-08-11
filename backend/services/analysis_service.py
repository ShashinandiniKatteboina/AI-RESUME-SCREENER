from services.matching_service import generate_match_result


def analyze_resume(resume, job_description, required_skills):

    # --------------------------------------------------------
    # Match resume with job
    # --------------------------------------------------------

    result = generate_match_result(
        resume,
        required_skills
    )

    # --------------------------------------------------------
    # Return complete matching result
    # --------------------------------------------------------

    return {
        "job_description": job_description,

        "required_skills": required_skills,

        "match_score": result["match_score"],

        "matched_skills": result["matched_skills"],

        "missing_skills": result["missing_skills"],

        "skill_gap": result["skill_gap"],

        "total_required_skills": result["total_required_skills"],

        "total_matched_skills": result["total_matched_skills"],

        "total_missing_skills": result["total_missing_skills"]
    }