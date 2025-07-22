**1. PROJECT OVERVIEW**  
This system parses user uploaded resumes (PDF, DOCX, SCANNED IMAGES) extracts structured information using NLP and OCR , and matches them against predefined job descriptions to compute a match score. A web interface facilitates interaction.



**2. FUNCTIONAL REQUIREMENTS**
| Feature                              | Description                                                                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Resume Upload**                    | Users can upload `.pdf`, `.docx`, or image-based resumes.                                                                                        |
| **OCR Parsing**                      | Use Tesseract OCR for image-based resumes (scanned/photographed).                                                                                |
| **NLP Information Extraction**       | Extract Name, Email, Phone, Skills, Education, Work Experience using spaCy or transformers.                                                      |
| **Section Classification**           | Classify text blocks into logical sections (e.g., Education, Work Experience).                                                                   |
| **Skill Extraction**                 | Use keyword matching and NLP to identify relevant skills.                                                                                        |
| **Job Description Upload/Selection** | Allow selection of a predefined job role or upload a JD.                                                                                         |
| **Job Match Score Calculation**      | Use cosine similarity or BERT embeddings to compare resume vs. job description.                                                                  |
| **Web Dashboard**                    | Simple, clean Flask/Django frontend to: <br> - Upload resume <br> - Display parsed info <br> - Show matching score <br> - Download parsed output |
| **Download Output**                  | Option to download parsed info as `.txt` or `.json` for reuse.                                                                                   |


**3.USER WORKFLOW**   

![IRP Mworkflow](https://github.com/user-attachments/assets/526e8a4f-0e38-4c68-be88-3822c25d1b1c)


**4. SYSTEM MODULES**  
**A. OCR PIPELINE:**    
Library: Tesseract OCR, OpenCV    
Input: Scanned resume image    
Output: Raw text 

**B. NLP PARSER:**  
Library: spaCy or HuggingFace Transformers   
Tasks: NER, skill extraction, section classification  

**C. JOB MATCHING ENGINE**    
Logic: Cosine similarity or BERT embeddings  
Library: sentence-transformers  
Output: Score (0-100) , matched skill list   

**D. WEB FRONTEND**  
Framewrok: Flask or Django   
UI: Bootstrap   
Views: Upload form , output page , download option    




**5. DEPENDENCIES**   
Python 3.10+   
Tesseract OCR (installed separately)   
OpenCV   
spaCy or HuggingFace Transformers    
sentence-transformers   
Flask or Django    
SQLite or local JSON   



**6. OUTPUT FORMAT:**      
Display structured resume summary on-screen.    
Save/download output as `.txt`,`.json` or database record.    
Job match score and relevant keyword overlaps shown.    


