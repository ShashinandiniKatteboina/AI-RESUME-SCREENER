def normalize_skill(skill):

    skill = skill.lower().strip()

    aliases = {
        "node js": "node.js",
        "nodejs": "node.js",

        "express": "express.js",

        "postgres": "postgresql",
        "postgre sql": "postgresql",

        "mongo": "mongodb",

        "js": "javascript",

        "ts": "typescript",

        "rest api": "rest api",
        "rest apis": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",

        "dsa": "data structures",
        "data structures and algorithms": "data structures"
    }

    return aliases.get(skill, skill)


def get_resume_skills(resume):

    skills = []

    # 1. Skills from SKILLS section
    for category_skills in resume.get("skills", {}).values():
        skills.extend(category_skills)

    # 2. Skills from PROJECTS
    for project in resume.get("projects", []):

        tech_stack = project.get("tech_stack", [])

        skills.extend(tech_stack)

    # 3. Skills from EXPERIENCE
    for experience in resume.get("experience", []):

        if isinstance(experience, dict):

            # If experience has an explicit skills field
            experience_skills = experience.get("skills", [])

            skills.extend(experience_skills)

    return skills

def compare_skills(resume, job_skills):

    resume_skills = get_resume_skills(resume)

    # Normalize resume skills
    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    # Normalize job skills
    job_skill_set = {
        normalize_skill(skill)
        for skill in job_skills
    }

    # Find matched skills
    matched_skills = [
        skill
        for skill in job_skills
        if normalize_skill(skill) in resume_skill_set
    ]

    # Find missing skills
    missing_skills = [
        skill
        for skill in job_skills
        if normalize_skill(skill) not in resume_skill_set
    ]

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


def calculate_match_score(job_skills, matched_skills):

    if not job_skills:
        return 0

    score = (len(matched_skills) / len(job_skills)) * 100

    return round(score, 2)

def generate_match_result(resume, job_skills):

    comparison = compare_skills(resume, job_skills)

    matched_skills = comparison["matched_skills"]
    missing_skills = comparison["missing_skills"]

    score = calculate_match_score(
        job_skills,
        matched_skills
    )

    return {
        "match_score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": len(job_skills),
        "total_matched_skills": len(matched_skills),
        "total_missing_skills": len(missing_skills)
    }