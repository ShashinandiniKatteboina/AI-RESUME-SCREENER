from services.job_service import create_job


job_description = """
Software Engineer

We are looking for a candidate with strong knowledge of
Java, Python, SQL, Node JS, MongoDB, Git, React and RESTful APIs.

The candidate should also have good problem-solving skills.
"""


job = create_job(job_description)


print("===== JOB =====")

print("Description:")
print(job["description"])

print("\nRequired Skills:")

for skill in job["required_skills"]:
    print(skill)