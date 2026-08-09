import re


SKILLS = [
    "python",
    "java",
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
    "flask",
    "django",
    "spring boot",
    "mongodb",
    "mysql",
    "postgresql",
    "sql",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "data structures",
    "algorithms"
]
SKILL_ALIASES = {
    "node.js": ["node.js", "nodejs", "node js"],
    "express.js": ["express.js", "expressjs", "express js"],
    "mongodb": ["mongodb", "mongo db", "mongo"],
    "javascript": ["javascript", "java script", "js"],
    "typescript": ["typescript", "type script", "ts"],
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql", "my sql"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": ["natural language processing", "nlp"]
}

def extract_skills(text):

    text = text.lower()

    found_skills = []

    # Check aliases
    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    # Check normal skills
    for skill in SKILLS:

        if skill in SKILL_ALIASES:
            continue

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills