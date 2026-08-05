# AI Resume Screening and Intelligent Job Matching Platform

## Project Overview

### Problem Statement

Recruiters receive hundreds or even thousands of resumes for a single job opening. Manually reviewing every resume is time-consuming, and traditional Applicant Tracking Systems (ATS) often rely on simple keyword matching, which can overlook qualified candidates.

Candidates also struggle to understand how well their resumes match a job description, what skills they are missing, and how they can improve their chances of getting shortlisted.

This project aims to solve these problems by building an AI-powered platform that automatically analyzes resumes, matches them with job descriptions, identifies missing skills, and provides intelligent recommendations using NLP and Generative AI.

---

## Target Users

### Candidate

A candidate can:

- Register and log in
- Upload a resume (PDF)
- View extracted resume information
- View matched jobs
- Check resume-job match score
- View missing skills
- Receive AI-generated recommendations
- Get interview preparation suggestions

### Recruiter

A recruiter can:

- Register and log in
- Create job postings
- Upload job descriptions
- View candidate profiles
- Compare applicants
- Rank candidates based on match score
- View AI-generated candidate summaries

---

# Objectives

The primary objectives of this project are:

- Automate resume screening
- Reduce recruiter workload
- Improve candidate-job matching
- Identify candidate skill gaps
- Provide AI-powered recommendations
- Build a scalable recruitment platform

---

# Main Features

## Resume Management

- Upload PDF resumes
- Extract text from PDF
- Store resumes securely
- Parse resume information

---

## Resume Parsing

Extract:

- Name
- Email
- Phone Number
- Skills
- Education
- Experience
- Projects
- Certifications
- Social Links

---

## Job Management

- Create job postings
- Upload job descriptions
- Extract required skills
- Store jobs in database

---

## Resume-Job Matching

- Compare resume skills with job requirements
- Calculate match score
- Display matching percentage
- Rank candidates

---

## Skill Gap Analysis

Identify:

- Missing skills
- Matching skills
- Strong areas
- Weak areas

---

## AI Features

Using Gemini API:

- Resume summary
- Candidate strengths
- Missing skills explanation
- Learning recommendations
- Interview questions
- Career suggestions

---

## Dashboard

### Candidate Dashboard

- Resume details
- Extracted skills
- Match score
- Skill gap analysis
- AI recommendations

### Recruiter Dashboard

- Job postings
- Candidate list
- Candidate ranking
- Match scores
- Resume summaries

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| React.js | Frontend Development |
| JavaScript | Frontend Logic |
| HTML/CSS | User Interface |
| Python | Backend Development |
| Flask | REST API Framework |
| MongoDB Atlas | Database |
| pdfplumber | PDF Text Extraction |
| spaCy | Natural Language Processing |
| scikit-learn | TF-IDF & Cosine Similarity |
| Sentence Transformers | Semantic Matching |
| Gemini API | AI Summaries & Recommendations |
| Git | Version Control |
| GitHub | Code Repository |
| Render | Backend Deployment |
| Vercel | Frontend Deployment |

---

# System Workflow

```text
Candidate Uploads Resume (PDF)
            │
            ▼
Resume Text Extraction
            │
            ▼
Resume Information Extraction
            │
            ▼
Skill Extraction
            │
            ▼
Store Data in MongoDB
            │
            ▼
Recruiter Uploads Job Description
            │
            ▼
Job Description Processing
            │
            ▼
Resume-Job Matching
            │
            ▼
Match Score Calculation
            │
            ▼
Gemini AI Analysis
            │
            ▼
Display Results on Dashboard
```

---

# Future Enhancements

- ATS Resume Score
- Resume Improvement Suggestions
- Cover Letter Generator
- Resume Version Comparison
- Multiple Resume Upload
- Email Notifications
- Resume Analytics Dashboard
- AI Chat Assistant
- Multi-language Resume Support
- Vector Database Integration
- Advanced Semantic Search
- Admin Dashboard

---

# Expected Learning Outcomes

By completing this project, I will learn:

- Full Stack Web Development
- REST API Development
- Flask Framework
- React Development
- MongoDB Database Design
- Authentication & Authorization
- File Upload Handling
- PDF Parsing
- Natural Language Processing (NLP)
- Machine Learning Techniques
- Semantic Search
- Prompt Engineering
- Gemini API Integration
- Git & GitHub
- Deployment of Full Stack Applications

---

# End Goal

Build a production-quality AI Resume Screening and Intelligent Job Matching Platform that demonstrates:

- Strong Full Stack Development skills
- NLP knowledge
- Machine Learning concepts
- Generative AI integration
- Clean software architecture
- Real-world problem-solving ability

The completed project should be suitable for showcasing on GitHub, adding to my resume, and explaining confidently during technical interviews.