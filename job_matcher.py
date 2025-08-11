import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_parser import parse_resume  
from resume_extractor import extract_text_from_pdf, extract_text_from_docx, extract_text_from_image
from tkinter import filedialog, Tk
import os

def extract_skills_from_resume():
    chooser = Tk()
    chooser.withdraw()
    file_path = filedialog.askopenfilename(
        title="Choose Resume File",
        filetypes=[("PDF files", "*.pdf"), ("Word Documents", "*.docx"), ("Images", "*.jpg *.png *.jpeg")]
    )

    if not file_path:
        print("No file selected.")
        return []

    if file_path.lower().endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        raw_text = extract_text_from_docx(file_path)
    elif any(file_path.lower().endswith(ext) for ext in [".jpg", ".png", ".jpeg"]):
        raw_text = extract_text_from_image(file_path)
    else:
        print("Unsupported file format.")
        return []
    parsed_output = parse_resume(raw_text)
    return parsed_output.get("skills", [])

def fetch_job_descriptions(database_file):
    try:
        connection = sqlite3.connect(database_file)
        cursor=connection.cursor()
        cursor.execute("SELECT id, title, description FROM job_descriptions")
        records = cursor.fetchall()
        connection.close()
        return records
    except sqlite3.Error as error:
        print("problem in accessing the database", error)
        return []
def find_job_match(resume_keywords, job_data, top_n=3):
    texts=[job[2] for job in job_data]
    texts.append(" ".join(resume_keywords))
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    resume_vector = tfidf_matrix[-1]
    job_vectors = tfidf_matrix[:-1]
    similarity_score = cosine_similarity(resume_vector,job_vectors)[0]
    job_scores =[(job_data[i][0], job_data[i][1], similarity_score[i] * 100) for i in range(len(job_data))]
    ranked_jobs = sorted(job_scores, key=lambda x: x[2], reverse=True)
    return ranked_jobs[:top_n]

def display_job_matches(matches):
    print("\nBest Matching Job Roles:\n")
    for job_id, title, score in matches:
        print(f"{title} (Match Score: {score:.2f}%)")
if __name__ == "__main__":
    print("\nMatching your resume to the best fitting job roles\n")
    extracted_skills = extract_skills_from_resume()
    print(f"\nExtracted Skills: {', '.join(extracted_skills)}")

    if not extracted_skills:
        print("No skills found in the resume.")
    else:
        job_data = fetch_job_descriptions("jobs.db")
        if job_data:
            print("\navailable Job Titles:")
            for job in job_data:
                print(f"{job[0]}. {job[1]}")
            try:
                selected_id = int(input("\nenter the Job ID you want to match against: "))
                selected_job = next((job for job in job_data if job[0] == selected_id), None)
                if selected_job:
                    matches = find_job_match(extracted_skills, [selected_job], top_n=1)
                    print(f"\nExtracted Skills: {', '.join(extracted_skills)}")
                    display_job_matches(matches)
                else:
                    print("invalid job ID selected.")
            except ValueError:
                print("please enter a valid numeric Job ID.")
        else:

            print("no jobs available in the system.")
