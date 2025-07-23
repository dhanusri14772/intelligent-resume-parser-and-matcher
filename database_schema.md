**Database schema for intelligent resume parser and job matcher:**  
This document outlines the database schema design for storing resume data , job description , and job-resume match results.


**Table 1:** `Resumes`

stores parsed information from each uploaded resume.

| Field         | Type      | Description                        |
|---------------|-----------|------------------------------------|
| resume_id     | INTEGER   | Primary Key                        |
| name          | TEXT      | Candidate name                     |
| email         | TEXT      | Email address                      |
| phone         | TEXT      | Phone number                       |
| education     | TEXT      | Education section (cleaned)        |
| experience    | TEXT      | Work experience section            |
| skills        | TEXT      | Comma-separated extracted skills   |
| raw_text      | TEXT      | Full resume content (optional)     |
| uploaded_at   | DATETIME  | Timestamp when resume was uploaded |


**Table 2:** `Job Description`

stores predefined job descriptions for matching.

| Field            | Type      | Description                    |
|------------------|-----------|--------------------------------|
| job_id           | INTEGER   | Primary Key                    |
| title            | TEXT      | Job title                      |
| description      | TEXT      | Full job description text      |
| skills_required  | TEXT      | Required skills (comma-separated) |


**Table 3:** `match results`

stores matching scores between resumes and job descriptions.

| Field            | Type      | Description                            |
|------------------|-----------|----------------------------------------|
| match_id         | INTEGER   | Primary Key                            |
| resume_id        | INTEGER   | Foreign Key → `resumes.resume_id`      |
| job_id           | INTEGER   | Foreign Key → `job_descriptions.job_id`|
| match_score      | REAL      | Match percentage (0 to 100)            |
| matched_skills   | TEXT      | Skills that overlapped                 |
| evaluated_at     | DATETIME  | Timestamp when match was calculated    |



**Storage Engine**  
Database type: SQLite (for local dev) or JSON files (simple version).
Each table maps to a python dictionary or SQL table depending on backend.


