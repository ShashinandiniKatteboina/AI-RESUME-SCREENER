from services.job_parser import extract_job_skills


job_description = """
We are looking for a Software Engineer.

Requirements:
- Strong knowledge of Java and Python
- SQL experience
- Data Structures and Algorithms
- REST API development
- MongoDB
- Git and GitHub
"""


skills = extract_job_skills(job_description)


print("===== JOB SKILLS =====")

for skill in skills:
    print(skill)