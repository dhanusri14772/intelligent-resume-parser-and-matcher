import sqlite3

def connect_to_database(db_name):
    try:
        connection = sqlite3.connect(db_name)
        print(f"conected to database : {db_name}")
        return connection
    except sqlite3.Error as e :
        print("error while connecting to database:", e)
        return None
def create_table(connection):
    try:
        cursor=connection.cursor()
        sql_statement ="""
         CREATE TABLE IF NOT EXISTS job_descriptions (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         description TEXT NOT NULL)"""
        cursor.execute(sql_statement)
        connection.commit()
    except sqlite3.Error as e:
        pass
def insert_sample_jobs(connection):
        job_entries=[
             (
        "Data Scientist","Analyze large datasets using Python, pandas, and SQL. Build machine learning models with scikit-learn and visualize insights using matplotlib and seaborn. Familiarity with Jupyter, statistics, and data storytelling is essential.",
        "Backend Developer","Develop RESTful APIs using Python and Flask or Node.js. Work with SQL and NoSQL databases like MySQL and MongoDB. Use Git for version control and deploy backend services with Docker.",
        "Frontend Developer","Create responsive UI using HTML, CSS, and JavaScript. Experience with frontend frameworks like React or Angular. Use Git for versioning and consume APIs for dynamic data rendering.",
        "AI Engineer","Design and deploy AI models using TensorFlow, PyTorch, and Keras. Strong skills in Python, computer vision, NLP, and deep learning required. Work in Jupyter/Colab with datasets using pandas and NumPy.",
        "DevOps Engineer","Automate deployments using CI/CD pipelines. Use tools like Docker, Jenkins, and Kubernetes. Proficient in Linux, Git, and cloud platforms such as AWS and Azure.",
        "Cybersecurity Analyst", "Monitor security threats and respond using tools like Wireshark and firewalls. Understand cryptography, penetration testing, and secure coding. Familiar with OS fundamentals and networking protocols.",
        "Database Administrator", "Administer relational databases like MySQL, PostgreSQL, and NoSQL like MongoDB. Perform backups, tuning, and data modeling. Use SQL extensively for querying and data integrity checks.",
        "Full Stack Developer","Work across frontend (HTML, CSS, JavaScript, React) and backend (Python, Node.js, MySQL). Build full-stack apps, integrate APIs, and use Git, Docker, and cloud services.",
        "Machine Learning Engineer","Build and deploy ML models using scikit-learn, TensorFlow, or PyTorch. Proficient in Python, feature engineering, pandas, NumPy, and Jupyter. Experience with model evaluation, versioning, and deployment.",
        "Software Tester", "Write and execute test cases. Automate tests using Selenium or PyTest. Identify bugs, ensure quality with manual and automated testing. Understand SDLC, version control using Git."
    )]
        try:
            cursor = connection.cursor()
            cursor.executemany("insert into job_descriptions (title, description) values(?,?)", job_entries)
            connection.commit()
        except sqlite3.Error as e:
            print("error in inserting data", e)
def close_connection(connection):
        if connection:
            connection.close()
            print("connection to database closed.")
def setup_job_db():
     db_name = "jobs.db"
     conn = connect_to_database(db_name)
     if conn:
          create_table(conn)
          insert_sample_jobs(conn)

if __name__ =="__main__":
  print("intialized job description database")
  setup_job_db()
   