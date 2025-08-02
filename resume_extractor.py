import os
import fitz
import docx
import cv2
import pytesseract
from PIL import Image
from tkinter import Tk, filedialog

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
       with fitz.open(pdf_path)as doc:
           for page in doc:
               text += page.get_text()
       return text
    except Exception as e:
        print(f"error extracting text from pdf : {e}")
        return ""
    
def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        print(f"error extracting text from docx: {e} ")
        return ""    
def extract_text_from_image(image_path):
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text
    except Exception as e:
        print(f"error extracting text from image: {e}")
        return ""
def clean_text(text):
    return text.strip()

if __name__== "__main__":
    print("intelligent resume text extractor")
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="select a resume file", filetypes=[("Supported Files", "*.pdf *.docx *.png *.jpg *.jpeg")])
    if not file_path:
        print("no file selected")
    elif file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
         text = extract_text_from_image(file_path)
    else:
        print("unsupported file type")
        text = ""

    if text:
        cleaned = clean_text(text)
        print("extracted resume text")
        print(cleaned)
        