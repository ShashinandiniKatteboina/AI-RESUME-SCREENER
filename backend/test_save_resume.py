from services.pdf_service import extract_text_from_pdf
from services.resume_parser import parse_resume
from database.resume_repository import save_resume


pdf_path = "uploads/23b81a05dp_resume-2.pdf"


# Extract text from PDF
text = extract_text_from_pdf(pdf_path)


# Parse resume
resume = parse_resume(text)


# Save to MongoDB
resume_id = save_resume(resume)


print("✅ Resume saved successfully")
print("Resume ID:", resume_id)