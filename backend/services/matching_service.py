def get_resume_skills(resume):

    skills = []

    for category_skills in resume.get("skills", {}).values():
        skills.extend(category_skills)

    return skills


def compare_skills(resume, job_skills):

    resume_skills = get_resume_skills(resume)

    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    job_skill_set = {
        normalize_skill(skill)
        for skill in job_skills
    }

    matched_skills = [
        skill for skill in job_skills
        if normalize_skill(skill) in resume_skill_set
    ]

    missing_skills = [
        skill for skill in job_skills
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