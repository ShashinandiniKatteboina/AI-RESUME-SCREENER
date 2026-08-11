from services.ai_service import generate_ai_analysis


resume = {
    "name": "K.SHASHI NANDINI",
    "skills": {
        "Languages": [
            "Java",
            "Python",
            "SQL",
            "C",
            "Data Structures"
        ],
        "Web & Backend Technologies": [
            "HTML",
            "CSS",
            "JavaScript",
            "Node.js",
            "Express.js",
            "MongoDB"
        ]
    }
}


job_description = """
Software Engineer

Requirements:
Java
Python
SQL
React
MongoDB
Git
Data Structures
"""


result = generate_ai_analysis(
    resume=resume,
    job_description=job_description,
    match_score=71.43,
    matched_skills=[
        "Java",
        "Python",
        "SQL",
        "MongoDB",
        "Data Structures"
    ],
    missing_skills=[
        "React",
        "Git"
    ]
)


print("===== AI ANALYSIS =====")
print(result)