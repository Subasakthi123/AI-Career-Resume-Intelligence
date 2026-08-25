"""
Resume Scorer Module

This module evaluates resumes based on three criteria:
1. Job Skill Match (50% weight) - derived from job matching results.
2. Skill Coverage (25% weight) - breadth of skills across predefined categories.
3. Content Quality (25% weight) - presence of standard resume sections.
"""

import re
import logging
from src.skill_extractor import load_skills_dictionary

logger = logging.getLogger(__name__)

def calculate_resume_score(resume_text: str, resume_skills: dict, job_skills: dict, match_result: dict) -> dict:
    """
    Calculates a transparent overall resume score out of 100 based on weighted metrics.
    
    Args:
        resume_text (str): Raw extracted resume text.
        resume_skills (dict): Extracted resume skills.
        job_skills (dict): Extracted job description skills.
        match_result (dict): Output from match_resume_to_job.
        
    Returns:
        dict: A dictionary containing:
            - overall_score (float): Total score out of 100.
            - job_match_score (float): Score for skill matching (0-100).
            - skill_coverage_score (float): Score for skill breadth (0-100).
            - content_quality_score (float): Score for resume structure completeness (0-100).
            - detected_sections (list): List of detected resume sections.
    """
    # 1. Job Skill Match (50% Weight)
    job_match_score = match_result.get("match_percentage", 0.0)
    
    # 2. Skill Coverage (25% Weight)
    # Calculate how broadly the resume covers predefined skill categories.
    skills_dict = load_skills_dictionary()
    total_categories = len(skills_dict) if skills_dict else 8 # Fallback to 8
    
    # Count how many categories have at least one skill detected in the resume
    covered_categories = len(resume_skills)
    skill_coverage_score = (
        (covered_categories / total_categories) * 100 
        if total_categories > 0 
        else 0.0
    )
    
    # 3. Resume Content Quality (25% Weight)
    # Check for the presence of standard sections using regex
    sections_keywords = {
        "Education": r"\b(education|academic|degree|university|college|school|studies|diploma)\b",
        "Experience": r"\b(experience|employment|work history|professional history|career|history|experience|work|positions)\b",
        "Projects": r"\b(projects|portfolio|personal projects|key projects|academic projects)\b",
        "Skills": r"\b(skills|technical skills|expertise|competencies|abilities|technologies)\b",
        "Certifications": r"\b(certifications|certificates|credentials|courses|training|awards|accreditation)\b"
    }
    
    detected_sections = []
    if resume_text:
        for section, pattern in sections_keywords.items():
            if re.search(pattern, resume_text, re.IGNORECASE):
                detected_sections.append(section)
                
    # 20 points per section present (5 sections total = 100 points max)
    total_sections_count = len(sections_keywords)
    detected_count = len(detected_sections)
    content_quality_score = (
        (detected_count / total_sections_count) * 100 
        if total_sections_count > 0 
        else 0.0
    )
    
    # Calculate weighted overall score
    # 50% match + 25% coverage + 25% quality
    overall_score = (
        (job_match_score * 0.5) + 
        (skill_coverage_score * 0.25) + 
        (content_quality_score * 0.25)
    )
    
    return {
        "overall_score": round(overall_score, 2),
        "job_match_score": round(job_match_score, 2),
        "skill_coverage_score": round(skill_coverage_score, 2),
        "content_quality_score": round(content_quality_score, 2),
        "detected_sections": detected_sections
    }
