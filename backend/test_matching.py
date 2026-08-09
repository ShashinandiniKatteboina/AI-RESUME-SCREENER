from services.matching_service import (
    compare_skills,
    calculate_match_score
)


resume = {
    "skills": {
        "Languages": [
            "Java",
            "SQL",
            "Python",
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
        ],
        "Soft Skills": [
            "Problem Solving",
            "Time Management",
            "Communication",
            "Leadership"
        ]
    }
}


job_skills = [
    "Java",
    "Python",
    "SQL",
    "Node JS",
    "Mongo",
    "Git",
    "React",
    "RESTful APIs"
]


result = compare_skills(resume, job_skills)
score = calculate_match_score(
    job_skills,
    result["matched_skills"]
)

print("===== MATCHED SKILLS =====")

for skill in result["matched_skills"]:
    print(skill)


print("\n===== MISSING SKILLS =====")

for skill in result["missing_skills"]:
    print(skill)

print("\n===== MATCH SCORE =====")
print(f"{score}%")