import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_name(text):
    lines = text.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    for line in lines[:5]:  # only check first 5 lines
        # Skip lines with emails, links, or phone numbers
        if re.search(r'@|http|www|linkedin|(\+?\d[\d\s\-\(\)]{8,}\d)', line, re.IGNORECASE):
            continue

        # If line contains only letters and spaces, assume it's a name
        if re.match(r"^[A-Za-z ,.'-]+$", line) and len(line.split()) <= 4:
            return line.strip()

    return "Name not found"



# 🔽 Now this can safely use extract_name
def parse_resume(resume_text):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
    phone = re.findall(r"\+?\d[\d\s\-\(\)]{8,}\d", resume_text)
    name = extract_name(resume_text)

    return {
        "name": name,
        "email": email[0] if email else "N/A",
        "phone": phone[0] if phone else "N/A"
    }

