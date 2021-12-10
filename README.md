# Placement-Portal-Streamlit
DBMS-Project for semester 5 MIT MANIPAL


A Placement Portal 


A solution with 6 tables


+ job (details about the jobs)
+ branch (all the branches in the university)
+ students (details of the students applying)
+ company (details of the companies)
+ job_branch (details on which branch is eligible for which job)
+ selection (students placed)
        

The students login with the student portal and the admin fills in the company details, the job details of the registered companies, and the eligibility criteria. After the job is posted, the students can check the jobs for which they are eligible and apply to the same. The tables are updated automatically according to the information passed by the companies and selected students are added to the selected tables.

## Tech Stack
+ Streamlit-Python
+ MySql Database

# How to Run
+ Make a virtual environment of python3.7(Recommended)
+ Install the ```requirements.txt```
+ Use the command ```streamlit run app.py``` to run the application
