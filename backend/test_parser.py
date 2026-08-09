from services.pdf_service import extract_text_from_pdf,extract_links_from_pdf
from services.resume_parser import (
    extract_email,
    extract_phone,
    extract_contact_line,
    extract_name,
    extract_education_section,
    parse_education,
    extract_project_section,
    parse_projects,
    extract_skills_section,
    extract_certifications_section,
    parse_certifications,
    extract_experience_section,
    parse_resume
)

pdf_path = "uploads/23b81a05dp_resume-2.pdf"

text = extract_text_from_pdf(pdf_path)
links = extract_links_from_pdf(pdf_path)
contact_line = extract_contact_line(text)
name = extract_name(text)
education = extract_education_section(text)
parsed_education = parse_education(education)
projects = extract_project_section(text)
parsed_projects = parse_projects(projects)
skills_section = extract_skills_section(text)
certifications = extract_certifications_section(text)
parsed_certifications = parse_certifications(certifications)
experience = extract_experience_section(text)
resume = parse_resume(text)

'''print("===== EXTRACTED TEXT =====")
print(text)'''

print("\n===== RESUME CONTACT INFORMATION =====")

email = extract_email(text)
phone = extract_phone(text)
print("Name:", name)

print("Email:", email)
print("Phone:", phone)


print("\n===== CONTACT LINE =====")

for item in contact_line:
    print(item)

print("\n===== EDUCATION =====")

for line in education:
    print(line)

print("\n===== PARSED EDUCATION =====")

for entry in parsed_education:
    print(entry)

print("\n===== PROJECT SECTION =====")

for line in projects:
    print(line)

print("\n===== PARSED PROJECTS =====")

for project in parsed_projects:
    print(project)

print("\n===== PARSED SKILLS =====")

for category, skills in skills_section.items():
    print(category, ":", skills)

print("\n===== CERTIFICATION SECTION =====")

for line in certifications:
    print(line)

print("\n===== PARSED CERTIFICATIONS =====")

for certification in parsed_certifications:
    print(certification)

print("\n===== EXPERIENCE SECTION =====")

for line in experience:
    print(line)

print("\n===== COMPLETE STRUCTURED RESUME =====")

print(resume)