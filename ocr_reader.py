import pytesseract
from pdf2image import convert_from_path
from PIL import Image 
import os
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def ocr_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print("error in reading image")
        return""
def ocr_from_pdf(pdf_path):
    try:
        pages = convert_from_path(pdf_path,dpi=300)
        full_text = ""
        for i , page in enumerate(pages):
            temp_img_path = f"page_{i}.png"
            page.save(temp_img_path, "PNG")
            text = pytesseract.image_to_string(Image.open(temp_img_path))
            full_text+=text +"\n"
            os.remove(temp_img_path)
        return full_text
    except Exception as e:
        print("error reading pdf",e)
        return ""
    
if __name__ =="__main__" :
   from tkinter import filedialog, Tk
   root = Tk()
   root.withdraw()
   file_path = filedialog.askopenfilename(title="select image or scanned pdf")
   if file_path.endswith((".png",".jpg",".jpeg")):
      text = ocr_from_image(file_path)
   elif file_path.endswith(file_path):
      text = ocr_from_pdf(file_path)
   else:
      print ("unsuppoerted file type")
      text =""
   if text:
      print("\n ocr extracted text :\n")
      print(text)

                       
    
                      