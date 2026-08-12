# ============================================================
# NORMALIZE SKILL
# ============================================================

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


# ============================================================
# GET RESUME SKILLS
# ============================================================

def get_resume_skills(resume):

    skills = []

    # ========================================================
    # 1. Skills from structured SKILLS section
    # ========================================================

    resume_skills = resume.get("skills", {})

    if isinstance(resume_skills, dict):

        for category_skills in resume_skills.values():

            if isinstance(category_skills, list):
                skills.extend(category_skills)

    elif isinstance(resume_skills, list):

        skills.extend(resume_skills)

    # ========================================================
    # 2. Skills from PROJECTS
    # ========================================================

    projects = resume.get("projects", [])

    if isinstance(projects, list):

        for project in projects:

            if isinstance(project, dict):

                tech_stack = project.get(
                    "tech_stack",
                    []
                )

                if isinstance(tech_stack, list):
                    skills.extend(tech_stack)

    # ========================================================
    # 3. Skills from EXPERIENCE
    # ========================================================

    experience = resume.get("experience", [])

    if isinstance(experience, list):

        for experience_item in experience:

            if isinstance(experience_item, dict):

                experience_skills = experience_item.get(
                    "skills",
                    []
                )

                if isinstance(experience_skills, list):
                    skills.extend(experience_skills)

    # ========================================================
    # 4. FALLBACK — EXTRACT SKILLS FROM RESUME TEXT
    # ========================================================

    resume_text = resume.get("text", "")

    if resume_text:

        known_skills = [
            "Java",
            "Python",
            "C",
            "C++",
            "SQL",
            "JavaScript",
            "TypeScript",

            "HTML",
            "CSS",

            "Node.js",
            "Node JS",
            "Express.js",
            "Express",

            "React",
            "Tailwind CSS",

            "MySQL",
            "PostgreSQL",
            "MongoDB",

            "Git",
            "GitHub",
            "Docker",
            "Kubernetes",

            "AWS",
            "Azure",
            "GCP",

            "REST API",
            "REST APIs",
            "RESTful API",
            "RESTful APIs",

            "Data Structures",
            "Data Structures and Algorithms",

            "OOP",
            "Object-Oriented Programming",

            "DBMS",
            "Computer Networks",
            "Operating Systems",

            "Gemini API",
            "Prompt Engineering",
            "Resume Parsing"
        ]

        text_lower = resume_text.lower()

        for skill in known_skills:

            if skill.lower() in text_lower:

                skills.append(skill)

    return skills


# ============================================================
# COMPARE SKILLS
# ============================================================

def compare_skills(resume, job_skills):

    resume_skills = get_resume_skills(resume)

    # ========================================================
    # Normalize resume skills
    # ========================================================

    resume_skill_set = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    # ========================================================
    # Normalize job skills
    # ========================================================

    job_skill_set = {
        normalize_skill(skill)
        for skill in job_skills
    }

    # ========================================================
    # Find matched skills
    # ========================================================

    matched_skills = [

        skill

        for skill in job_skills

        if normalize_skill(skill)
        in resume_skill_set

    ]

    # ========================================================
    # Find missing skills
    # ========================================================

    missing_skills = [

        skill

        for skill in job_skills

        if normalize_skill(skill)
        not in resume_skill_set

    ]

    return {

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills

    }


# ============================================================
# CALCULATE MATCH SCORE
# ============================================================

def calculate_match_score(
    job_skills,
    matched_skills
):

    if not job_skills:
        return 0

    score = (
        len(matched_skills)
        / len(job_skills)
    ) * 100

    return round(score, 2)


# ============================================================
# GENERATE MATCH RESULT
# ============================================================

def generate_match_result(
    resume,
    job_skills
):

    comparison = compare_skills(
        resume,
        job_skills
    )

    matched_skills = comparison[
        "matched_skills"
    ]

    missing_skills = comparison[
        "missing_skills"
    ]

    skill_gap = analyze_skill_gap(
        missing_skills
    )

    score = calculate_match_score(
        job_skills,
        matched_skills
    )

    return {

        "match_score":
            score,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "skill_gap":
            skill_gap,

        "total_required_skills":
            len(job_skills),

        "total_matched_skills":
            len(matched_skills),

        "total_missing_skills":
            len(missing_skills)

    }


# ============================================================
# ANALYZE SKILL GAP
# ============================================================

def analyze_skill_gap(missing_skills):

    technical_keywords = {

        "java",
        "python",
        "sql",
        "c",
        "c++",

        "javascript",
        "typescript",

        "html",
        "css",

        "react",

        "node.js",
        "express.js",

        "mongodb",
        "postgresql",
        "mysql",

        "git",

        "docker",
        "kubernetes",

        "aws",
        "azure",
        "gcp",

        "rest api",

        "data structures",
        "algorithms"

    }

    technical = []
    soft = []

    for skill in missing_skills:

        normalized = normalize_skill(
            skill
        )

        if normalized in technical_keywords:

            technical.append(skill)

        else:

            soft.append(skill)

    return {

        "technical_skills":
            technical,

        "soft_skills":
            soft

    }