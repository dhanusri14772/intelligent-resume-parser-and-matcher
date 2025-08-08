from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from nlp_parser import parse_resume
from resume_extractor import extract_text_from_pdf,extract_text_from_docx,extract_text_from_image
from job_matcher import fetch_job_descriptions, find_job_match

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'
os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)

@app.route('/')
def upload_page():
    job_list = fetch_job_descriptions("jobs.db")
    return render_template('index.html',jobs=job_list)
@app.route('/process',methods=['POST'])
def process_resume():
    uploaded_file = request.files['resume']
    job_id = int(request.form.get('job_id'))

    if uploaded_file:
         filename=secure_filename(uploaded_file.filename)
         file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
         uploaded_file.save(file_path)
         if filename.lower().endswith('.pdf'):
             resume_text = extract_text_from_pdf(file_path)
         elif filename.lower().endswith('.docx'):
             resume_text= extract_text_from_docx(file_path)
         elif filename.lower().endswith('.jpg','.jpeg', '.png'):
             resume_text =extract_text_from_image(file_path)
         else:
             return 'unsupported filetype.'

         parsed_data = parse_resume(resume_text)
         skills = parsed_data.get('skills',[])
         job_list = fetch_job_descriptions("jobs.db")
         selected_job = [job for job in job_list if job[0] == job_id]

         if selected_job:
             matched_job = find_job_match(skills, selected_job, top_n=1) 
         else :
             matched_job = []

         return render_template("result.html" , parsed = parsed_data, match=matched_job)
    return 'no file uploaded'

if __name__ == '__main__':
  app.run(debug=True) 