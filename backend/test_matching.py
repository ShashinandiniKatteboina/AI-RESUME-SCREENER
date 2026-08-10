from services.matching_service import generate_match_result

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


result = generate_match_result(
    resume,
    job_skills
)

print("\n===== MATCHING RESULT =====")

print("Match Score:", result["match_score"], "%")

print("\nMatched Skills:")

for skill in result["matched_skills"]:
    print(skill)

print("\nMissing Skills:")

for skill in result["missing_skills"]:
    print(skill)

print("\nTotal Required Skills:",
      result["total_required_skills"])

print("Total Matched Skills:",
      result["total_matched_skills"])

print("Total Missing Skills:",
      result["total_missing_skills"])