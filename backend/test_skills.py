from services.pdf_service import extract_text_from_pdf
from services.skill_service import extract_skills


pdf_path = "uploads/23b81a05dp_resume-2.pdf"

text = extract_text_from_pdf(pdf_path)

skills = extract_skills(text)

print("===== EXTRACTED SKILLS =====")

for skill in skills:
    print(skill)