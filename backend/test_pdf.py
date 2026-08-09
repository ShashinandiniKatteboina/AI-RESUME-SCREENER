from services.pdf_service import extract_text_from_pdf


pdf_path = "uploads/23b81a05dp_resume-2.pdf"

text = extract_text_from_pdf(pdf_path)

print("===== EXTRACTED TEXT =====")
print(text)