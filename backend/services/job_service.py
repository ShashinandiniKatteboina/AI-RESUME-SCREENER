from services.skill_service import extract_skills


def process_job_description(description):

    """
    Extract required skills from a job description.
    """

    required_skills = extract_skills(description)

    return required_skills