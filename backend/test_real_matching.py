from database.resume_repository import get_resume
from services.matching_service import generate_match_result


# Resume stored in MongoDB
resume_id = "6a780c4278f66ba576a9084a"


# Get resume
resume = get_resume(resume_id)


if not resume:

    print("❌ Resume not found")

else:

    print("✅ Resume retrieved from MongoDB")

    # Example job requirements
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

    # Generate matching result
    result = generate_match_result(
        resume,
        job_skills
    )

    print("\n===== REAL RESUME MATCHING =====")

    print("\nMatch Score:",
          result["match_score"], "%")

    print("\nMatched Skills:")

    for skill in result["matched_skills"]:
        print(skill)

    print("\nMissing Skills:")

    for skill in result["missing_skills"]:
        print(skill)