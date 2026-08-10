from services.job_parser import extract_job_skills


def create_job(job_description):

    skills = extract_job_skills(job_description)

    job = {
        "description": job_description,
        "required_skills": skills
    }

    return job