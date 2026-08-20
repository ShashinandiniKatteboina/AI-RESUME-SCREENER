# ============================================================
# ANALYSIS SERVICE
# ============================================================

from typing import List, Dict, Any


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):

    if not isinstance(skill, str):
        return ""

    skill = skill.lower().strip()

    aliases = {

        # Programming languages
        "js": "javascript",
        "java script": "javascript",

        # TypeScript
        "ts": "typescript",
        "type script": "typescript",

        # Node.js
        "node js": "node.js",
        "nodejs": "node.js",

        # Express
        "express": "express.js",
        "expressjs": "express.js",

        # MongoDB
        "mongo": "mongodb",
        "mongo db": "mongodb",

        # PostgreSQL
        "postgres": "postgresql",
        "postgre": "postgresql",
        "postgre sql": "postgresql",

        # MySQL
        "my sql": "mysql",

        # Data Structures
        "dsa": "data structures",
        "data structure": "data structures",

        # Algorithms
        "algo": "algorithms",

        # REST
        "rest api": "rest api",
        "rest apis": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",

        # Machine Learning
        "ml": "machine learning",

        # Artificial Intelligence
        "ai": "artificial intelligence"
    }

    return aliases.get(
        skill,
        skill
    )


# ============================================================
# GET RESUME SKILLS
# ============================================================

def get_resume_skills(resume):

    skills = []

    # --------------------------------------------------------
    # Get parsed resume
    # --------------------------------------------------------

    parsed_resume = resume.get(
        "parsed_resume",
        {}
    )

    if not isinstance(
        parsed_resume,
        dict
    ):
        return skills

    # ========================================================
    # 1. SKILLS SECTION
    # ========================================================

    resume_skills = parsed_resume.get(
        "skills",
        {}
    )

    if isinstance(
        resume_skills,
        dict
    ):

        for category_skills in resume_skills.values():

            if isinstance(
                category_skills,
                list
            ):

                for skill in category_skills:

                    if isinstance(
                        skill,
                        str
                    ):

                        skills.append(
                            skill.strip()
                        )

    # ========================================================
    # 2. PROJECT TECH STACK
    # ========================================================

    projects = parsed_resume.get(
        "projects",
        []
    )

    if isinstance(
        projects,
        list
    ):

        for project in projects:

            if not isinstance(
                project,
                dict
            ):
                continue

            tech_stack = project.get(
                "tech_stack",
                []
            )

            if isinstance(
                tech_stack,
                list
            ):

                for skill in tech_stack:

                    if isinstance(
                        skill,
                        str
                    ):

                        skills.append(
                            skill.strip()
                        )

    # ========================================================
    # 3. EXPERIENCE SKILLS
    # ========================================================

    experience = parsed_resume.get(
        "experience",
        []
    )

    if isinstance(
        experience,
        list
    ):

        for experience_item in experience:

            if not isinstance(
                experience_item,
                dict
            ):
                continue

            experience_skills = experience_item.get(
                "skills",
                []
            )

            if isinstance(
                experience_skills,
                list
            ):

                for skill in experience_skills:

                    if isinstance(
                        skill,
                        str
                    ):

                        skills.append(
                            skill.strip()
                        )

    # ========================================================
    # REMOVE EMPTY SKILLS
    # ========================================================

    skills = [

        skill

        for skill in skills

        if skill
    ]

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique_skills = []

    seen = set()

    for skill in skills:

        normalized = normalize_skill(
            skill
        )

        if not normalized:
            continue

        if normalized not in seen:

            seen.add(
                normalized
            )

            unique_skills.append(
                skill
            )

    return unique_skills


# ============================================================
# COMPARE RESUME SKILLS WITH JOB SKILLS
# ============================================================

def compare_skills(
    resume,
    job_skills
):

    # --------------------------------------------------------
    # Get resume skills
    # --------------------------------------------------------

    resume_skills = get_resume_skills(
        resume
    )

    # --------------------------------------------------------
    # Normalize resume skills
    # --------------------------------------------------------

    normalized_resume_skills = {

        normalize_skill(skill)

        for skill in resume_skills

        if normalize_skill(skill)
    }

    # --------------------------------------------------------
    # Matched skills
    # --------------------------------------------------------

    matched_skills = []

    for job_skill in job_skills:

        normalized_job_skill = normalize_skill(
            job_skill
        )

        if normalized_job_skill in normalized_resume_skills:

            matched_skills.append(
                job_skill
            )

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    missing_skills = []

    for job_skill in job_skills:

        normalized_job_skill = normalize_skill(
            job_skill
        )

        if normalized_job_skill not in normalized_resume_skills:

            missing_skills.append(
                job_skill
            )

    return {

        "resume_skills":
            resume_skills,

        "job_skills":
            job_skills,

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

        return 0.0

    score = (
        len(matched_skills)
        /
        len(job_skills)
    ) * 100

    return round(
        score,
        2
    )


# ============================================================
# ANALYZE SKILL GAP
# ============================================================

def analyze_skill_gap(
    missing_skills
):

    technical_keywords = {

        "java",
        "python",
        "c",
        "c++",
        "c#",

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

        "sql",

        "git",
        "github",

        "docker",
        "kubernetes",

        "aws",
        "azure",
        "gcp",

        "rest api",

        "data structures",
        "algorithms",

        "machine learning",
        "artificial intelligence"
    }

    technical_skills = []

    soft_skills = []

    for skill in missing_skills:

        normalized = normalize_skill(
            skill
        )

        if normalized in technical_keywords:

            technical_skills.append(
                skill
            )

        else:

            soft_skills.append(
                skill
            )

    return {

        "technical_skills":
            technical_skills,

        "soft_skills":
            soft_skills
    }


# ============================================================
# GENERATE MATCH RESULT
# ============================================================

def generate_match_result(
    resume,
    job_skills
):

    # --------------------------------------------------------
    # Make sure job skills is a list
    # --------------------------------------------------------

    if not isinstance(
        job_skills,
        list
    ):

        job_skills = []

    # --------------------------------------------------------
    # Remove empty job skills
    # --------------------------------------------------------

    job_skills = [

        skill.strip()

        for skill in job_skills

        if isinstance(
            skill,
            str
        )
        and skill.strip()
    ]

    # --------------------------------------------------------
    # Compare skills
    # --------------------------------------------------------

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

    resume_skills = comparison[
        "resume_skills"
    ]

    # --------------------------------------------------------
    # Calculate match score
    # --------------------------------------------------------

    match_score = calculate_match_score(
        job_skills,
        matched_skills
    )

    # --------------------------------------------------------
    # Analyze skill gap
    # --------------------------------------------------------

    skill_gap = analyze_skill_gap(
        missing_skills
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "match_score":
            match_score,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "skill_gap":
            skill_gap,

        "resume_skills":
            resume_skills,

        "total_required_skills":
            len(job_skills),

        "total_matched_skills":
            len(matched_skills),

        "total_missing_skills":
            len(missing_skills)
    }