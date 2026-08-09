import re


def extract_job_skills(text):

    skills = []

    # Common technical skills
    skill_patterns = [
        "Java",
        "Python",
        "C",
        "C++",
        "JavaScript",
        "TypeScript",
        "SQL",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "Express.js",
        "MongoDB",
        "PostgreSQL",
        "MySQL",
        "Git",
        "GitHub",
        "Docker",
        "AWS",
        "Azure",
        "Data Structures",
        "Algorithms",
        "REST API",
        "Machine Learning",
        "TensorFlow",
        "PyTorch"
    ]

    for skill in skill_patterns:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text, re.IGNORECASE):

            skills.append(skill)

    return skills