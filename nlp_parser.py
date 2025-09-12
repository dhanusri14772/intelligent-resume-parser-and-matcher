import spacy
import re
import pytesseract
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
nlp = spacy.load("en_core_web_sm")
SKILL_KEYWORDS = [
    "python", "java", "c++", "r", "sql", "javascript", "c", "deluge", "go",
    "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "excel",
    "tableau", "power bi", "machine learning", "deep learning", "nlp", "tensorflow",
    "keras", "computer vision", "jupyter", "googlecolab", "vscode", "colab",
    "mysql", "mongodb", "postgresql", "aws", "azure", "docker", "git"
]
def extract_name(text):
    false_positives = ["python", "java", "sql", "c++", "r", "machine learning", "matplotlib", "tableau"]
    lines = text.strip().split("\n")

    for i in range(min(5, len(lines))):
        line = lines[i].strip()
        if not line or "@" in line or any(char.isdigit() for char in line):
            continue
        if line.lower() in false_positives or len(line.split()) > 5:
            continue
        return line

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text.lower() not in false_positives:
            return ent.text.strip()

    return ""  
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0) if match else ""

def extract_phone(text):
    match = re.search(r"(\+91[\s\-]?)?[6-9]\d{9}", text)
    return match.group(0) if match else ""

def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text and skill not in found_skills:
            found_skills.append(skill)
    return found_skills 
def extract_education(text):
    lines = text.split("\n")
    education_section = []
    capture = False
    for line in lines:
        if "education" in line.lower():
            capture = True
            continue
        if capture:
            if line.strip() == "" or any(heading in line.lower() for heading in ["experience", "project", "skills", "certification"]):
                break
            education_section.append(line.strip())
    return education_section if education_section else []
def extract_experience(text):
    experience_titles = []
    start_keywords = ["project experiences", "projects", "experience", "work experience", "internship","Work Experience"]
    end_keywords = ["skills", "education", "certifications", "language", "about", "summary", "extra curricular", "achievements"]
    text_lower = text.lower()
    start_idx = -1
    for kw in start_keywords:
        start_idx = text_lower.find(kw)
        if start_idx != -1:
            break
    if start_idx == -1:
        return []
    sliced_text = text[start_idx:]
    end_idx = len(sliced_text)
    for end_kw in end_keywords:
        temp_idx = sliced_text.lower().find(end_kw)
        if temp_idx != -1:
            end_idx = min(end_idx, temp_idx)

    experience_block = sliced_text[:end_idx].strip()
    lines = experience_block.split("\n")
    for line in lines:
        clean = line.strip()
        if re.match(r"^\d+\.\s*", clean): 
            experience_titles.append(clean)
        elif len(clean.split()) >= 3 and clean[-1] != "." and clean[0].isupper():
            experience_titles.append(clean)

    return experience_titles if experience_titles else []

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text
def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
if __name__ == "__main__":
    from resume_extractor import extract_text_from_docx, extract_text_from_pdf, extract_text_from_image
    from tkinter import Tk, filedialog
    print("Intelligent Resume NLP Parser")
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select resume")
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_from_image(file_path)
    else:
        print("Unsupported file type")
        text = ""
    if text:
        parsed = parse_resume(text)
        print("Parsed Resume Data:\n")
        for key, value in parsed.items():
            print(f"{key.upper()}: {value}\n")
