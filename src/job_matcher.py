"""
Job Matcher Module

This module matches extracted resume skills with job description requirements,
calculating matching skills, missing skills, and match percentages.
"""

def match_resume_to_job(resume_skills: dict, job_skills: dict) -> dict:
    """
    Compares resume skills with job description requirements.
    
    Args:
        resume_skills (dict): Extracted resume skills grouped by category.
        job_skills (dict): Extracted job description skills grouped by category.
        
    Returns:
        dict: A dictionary containing:
            - match_percentage (float): Percentage of job skills matched.
            - matching_skills (dict): Matched skills grouped by category.
            - missing_skills (dict): Missing skills grouped by category.
            - total_job_skills (int): Total number of skills required by the job.
            - total_matched_skills (int): Total number of skills matched.
    """
    if not job_skills:
        return {
            "match_percentage": 0.0,
            "matching_skills": {},
            "missing_skills": {},
            "total_job_skills": 0,
            "total_matched_skills": 0
        }
        
    # Flatten resume skills for easy case-insensitive lookup
    resume_skills_lower = {
        skill.lower() for cat_skills in resume_skills.values() for skill in cat_skills
    }
    
    matching_skills = {}
    missing_skills = {}
    
    total_job_skills = 0
    total_matched_skills = 0
    
    for category, skills in job_skills.items():
        cat_matching = []
        cat_missing = []
        
        for skill in skills:
            total_job_skills += 1
            if skill.lower() in resume_skills_lower:
                cat_matching.append(skill)
                total_matched_skills += 1
            else:
                cat_missing.append(skill)
                
        if cat_matching:
            matching_skills[category] = cat_matching
        if cat_missing:
            missing_skills[category] = cat_missing
            
    match_percentage = (
        (total_matched_skills / total_job_skills) * 100 
        if total_job_skills > 0 
        else 0.0
    )
    
    return {
        "match_percentage": round(match_percentage, 2),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "total_job_skills": total_job_skills,
        "total_matched_skills": total_matched_skills
    }
