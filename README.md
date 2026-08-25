# AI Career & Resume Intelligence Platform

An intelligent resume analysis platform that helps candidates understand how well their resume matches a target job description, identify missing skills, evaluate resume quality, and receive actionable career recommendations.

## 🚀 Live Demo

https://ai-career-resume-intelligence-pecwvv54eyylhxvpdapptnp.streamlit.app/

## 📌 GitHub Repository

https://github.com/Subasakthi123/AI-Career-Resume-Intelligence

---

## 📖 Project Overview

Job seekers often struggle to understand whether their resume matches a particular job role and which skills they need to improve.

The **AI Career & Resume Intelligence Platform** provides an automated resume analysis workflow.

Users can upload a PDF resume and provide a target job description. The system extracts the resume content, identifies professional skills, compares them with job requirements, calculates a weighted analysis score, highlights skill gaps, and provides career improvement recommendations.

---

## 🎯 Problem Statement

Traditional resume checking requires manually comparing a resume with each job description.

This can make it difficult for candidates to:

- Identify missing technical skills
- Understand job-role requirements
- Measure resume-job alignment
- Improve resume content
- Decide which skills to learn next
- Choose suitable portfolio projects

This project provides a simple automated solution for these challenges.

---

## 💡 Solution

The platform analyzes both the candidate's resume and the target job description.

It then provides:

- Extracted resume text
- Detected resume skills
- Required job skills
- Matching skills
- Missing skills
- Resume analysis score
- Skill improvement recommendations
- Portfolio project suggestions
- Career and interview preparation suggestions

---

## ✨ Key Features

### 📄 Resume PDF Analysis

- Upload a PDF resume
- Extract text from all pages
- Handle empty or invalid PDF files gracefully

### 🧠 Skill Extraction

Identifies skills from the resume using a predefined JSON-based skill dictionary.

Skills are organized into categories such as:

- Programming Languages
- Data Science
- Machine Learning
- Web Development
- Databases
- Cloud
- Tools
- Soft Skills

### 🎯 Job Description Analysis

Extracts relevant skills from a target job description and categorizes them.

### 🔍 Skill Matching

Compares resume skills with job requirements and identifies:

- Matching skills
- Missing skills
- Skill gaps

### 📊 Resume Analysis Score

The platform calculates a weighted profile score using:

- Job Skill Match — 50%
- Skill Coverage — 25%
- Content Quality — 25%

The score is intended as an application-generated indicator and is not an official ATS or recruiter score.

### 🚀 Career Recommendations

Provides recommendations based on identified skill gaps, including:

- Skills to acquire
- Portfolio project ideas
- Resume improvement suggestions
- Career and interview preparation

---

## ⚙️ How It Works

```text
                ┌──────────────────────┐
                │    Upload Resume     │
                │       PDF File       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   PDF Text Extraction│
                │        pypdf          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Skill Extraction  │
                │   JSON + Regex Match │
                └──────────┬───────────┘
                           │
                           ▼
 ┌─────────────────────────┴─────────────────────────┐
 │                                                   │
 ▼                                                   ▼
┌─────────────────────┐                    ┌─────────────────────┐
│ Resume Skills       │                    │ Job Description     │
│                     │                    │ Skills              │
└──────────┬──────────┘                    └──────────┬──────────┘
           │                                          │
           └──────────────────┬───────────────────────┘
                              ▼
                   ┌─────────────────────┐
                   │   Skill Matching    │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Resume Score        │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Career              │
                   │ Recommendations     │
                   └─────────────────────┘
