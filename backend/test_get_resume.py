from database.resume_repository import get_resume


resume_id = "6a780c4278f66ba576a9084a"


resume = get_resume(resume_id)


if resume:

    print("===== RESUME FROM MONGODB =====")

    print("Name:", resume.get("name"))
    print("Email:", resume.get("email"))
    print("Phone:", resume.get("phone"))

    print("\nEducation:")
    print(resume.get("education"))

    print("\nSkills:")
    print(resume.get("skills"))

    print("\nProjects:")
    print(resume.get("projects"))

    print("\nCertifications:")
    print(resume.get("certifications"))

    print("\nExperience:")
    print(resume.get("experience"))

else:

    print("❌ Resume not found")