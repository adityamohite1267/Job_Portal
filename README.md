# ATS-Based Django Job Portal

This project is a role-based Job Portal web application built using Django and MySQL.
The system simulates how modern recruitment platforms work by allowing recruiters to post jobs evaluate resumes using an ATS match score system shortlist candidates and manage the hiring workflow

The main goal of this project was to understand how real-world job portals handle resume screening and recruiter decision-making processes.


# Project Features

# Role-Based Authentication

The system supports two types of users:

1. Recruiters
2. Jobseekers

Recruiters can post jobs and manage applicants while jobseekers can apply for jobs and track their application status.



# Job Posting System

Recruiters can:

1. Create job posts
2. Add required skills
3. Set job location
4. Activate or deactivate job listings

# Resume Upload and ATS Match Score

Jobseekers can upload resumes while applying.

The system extracts resume text and compares it with job-required skills to calculate a match score This helps simulate how an Applicant Tracking System filters candidates automatically

# Automatic Shortlisting Feature

If a candidate’s match score is above the defined threshold the system automatically marks the application as shortlisted This reduces manual effort for recruiters

# Recruiter Dashboard Analytics

Recruiters can view:

1. Total jobs posted
2. Total applications received
3. Number of shortlisted candidates
4. Number of rejected candidates
5. Number of hired candidates

This helps recruiters quickly understand the hiring pipeline.

# Application Status Workflow

Recruiters can update candidate status:

1. Shortlisted
3. Rejected
4. Hired

Applicants can track their application progress from their dashboard

# Email Notification System

Whenever a recruiter updates an application status the candidate receives an email notification automatically

The system sends notifications only when the status changes to avoid duplicate emails

# Duplicate Application Prevention

The system prevents users from applying multiple times for the same job using database-level constraints

# Technologies Used

Backend:

1. Python
2. Django

Frontend:

1. HTML
2. CSS
3. Bootstrap

Database:

* MySQL

Other Concepts Used:

1. Custom User Model
2. Django Signals
3. Resume text extraction logic
4. ATS match score calculation
5. Role-based dashboards

# What I Learned From This Project

While building this project I learned:

1. How to design a custom user model in Django
2. How recruiter and jobseeker workflows work internally
3. How resume screening logic can be implemented
4. How Django signals automate background tasks
5. How to build analytics dashboards
6. How to integrate MySQL with Django projects

This project helped me understand how real recruitment platforms manage candidate applications.

# Future Improvements

Planned improvements for this project:

1. OTP-based email verification during registration
2. Resume preview inside dashboard
3. Cloud deployment (Render)
4. AI-based job recommendation system

# Author

Aditya Mohite
Computer Science Engineering Student
