"""
AI Career Recommender Module

This module generates rule-based, actionable career and resume improvement
recommendations based on skills analysis, matching results, and scoring.
"""

def generate_recommendations(resume_text: str, resume_skills: dict, job_skills: dict, match_result: dict, score_result: dict) -> dict:
    """
    Generates actionable, structured recommendations to strengthen the candidate's profile.
    
    Args:
        resume_text (str): Raw resume text.
        resume_skills (dict): Extracted resume skills.
        job_skills (dict): Extracted job description skills.
        match_result (dict): Output from match_resume_to_job.
        score_result (dict): Output from calculate_resume_score.
        
    Returns:
        dict: A dictionary containing:
            - skills_to_learn (list): Specific skills to study.
            - resume_improvements (list): Sections/structure to fix.
            - project_ideas (list): Specific portfolio projects to build.
            - career_prep (list): Next steps for interview/career readiness.
    """
    recommendations = {
        "skills_to_learn": [],
        "resume_improvements": [],
        "project_ideas": [],
        "career_prep": []
    }
    
    # Extract missing skills list
    missing_by_cat = match_result.get("missing_skills", {})
    missing_skills_list = [skill for cat_skills in missing_by_cat.values() for skill in cat_skills]
    
    # Extract matching skills list
    matching_by_cat = match_result.get("matching_skills", {})
    matching_skills_list = [skill for cat_skills in matching_by_cat.values() for skill in cat_skills]
    
    # 1. Skills to Learn
    if not job_skills and not resume_skills:
        recommendations["skills_to_learn"].append(
            "Please upload a resume and job description to identify skills to acquire."
        )
    elif missing_skills_list:
        for skill in missing_skills_list[:5]: # Recommend up to 5 key skills
            recommendations["skills_to_learn"].append(
                f"Gain proficiency in **{skill}** as it is a required competency for this role."
            )
    else:
        recommendations["skills_to_learn"].append(
            "Great job! You have matched all the identified required skills for this job description."
        )
        
    # 2. Resume Improvements (based on missing sections and score)
    detected_sections = score_result.get("detected_sections", [])
    all_sections = ["Education", "Experience", "Projects", "Skills", "Certifications"]
    missing_sections = [s for s in all_sections if s not in detected_sections]
    
    for section in missing_sections:
        if section == "Projects":
            recommendations["resume_improvements"].append(
                "Add a **Projects** section to showcase practical applications of your technical capabilities."
            )
        elif section == "Certifications":
            recommendations["resume_improvements"].append(
                "Consider adding a **Certifications** section to feature relevant courses, licenses, or professional credentials."
            )
        elif section == "Experience":
            recommendations["resume_improvements"].append(
                "Your resume appears to lack an **Experience** (or Work History) section. Highlight jobs, internships, freelancing, or open-source contributions."
            )
        else:
            recommendations["resume_improvements"].append(
                f"Add a dedicated **{section}** section to improve the readability and structural score of your resume."
            )
            
    # Score-based improvements
    overall_score = score_result.get("overall_score", 0.0)
    if not job_skills and not resume_skills:
        recommendations["resume_improvements"].append(
            "Please upload a resume and paste a job description to get score-based improvements."
        )
    elif overall_score < 50:
        recommendations["resume_improvements"].append(
            "Your overall profile alignment is low. Focus on restructuring your layout, including missing core sections, and bridging critical skill gaps."
        )
    elif overall_score < 80:
        recommendations["resume_improvements"].append(
            "Refine your bullet points using the **STAR method** (Situation, Task, Action, Result) and highlight metrics where possible."
        )
    else:
        recommendations["resume_improvements"].append(
            "Your resume is highly optimized. Ensure your formatting is clean and consistent across all pages."
        )
        
    # 3. Project Ideas (based on missing skills)
    project_mappings = {
        "python": "Develop a multi-threaded web scraper or build a robust REST API using FastAPI/Django with automated testing.",
        "sql": "Design a relational database schema for an eCommerce store, insert mock dataset, and write optimized queries/indices.",
        "postgresql": "Design a relational database schema for an eCommerce store, insert mock dataset, and write optimized queries/indices.",
        "mysql": "Design a relational database schema for an eCommerce store, insert mock dataset, and write optimized queries/indices.",
        "machine learning": "Build an end-to-end ML pipeline (data cleaning, training, hyperparameter tuning) and host it via a Streamlit app.",
        "deep learning": "Implement an image classification or text generation model using PyTorch or TensorFlow, tracking experiments using TensorBoard.",
        "nlp": "Build a custom text classification or named entity recognition (NER) model using SpaCy or HuggingFace transformers.",
        "aws": "Host a static website on AWS S3 with CloudFront HTTPS, or build a serverless API using AWS Lambda, API Gateway, and DynamoDB.",
        "docker": "Containerize a multi-service web application (frontend, API, database) and write a docker-compose.yml for local orchestration.",
        "kubernetes": "Set up a local Kubernetes cluster (Minikube) and write deployment and service manifests to orchestrate container rollouts.",
        "git": "Contribute to open-source repositories or create public GitHub portfolios implementing clear branch branching models and PR reviews.",
        "github": "Contribute to open-source repositories or create public GitHub portfolios implementing clear branch branching models and PR reviews.",
        "react": "Develop a responsive dashboard interface with complex state management, data visualization charts, and REST API consumption.",
        "django": "Build a secure web platform using Django, complete with user authentication, database ORM, and API endpoints."
    }
    
    suggested_projects_count = 0
    for skill in missing_skills_list:
        lower_skill = skill.lower()
        if lower_skill in project_mappings:
            recommendations["project_ideas"].append(
                f"**Project for {skill}**: {project_mappings[lower_skill]}"
            )
            suggested_projects_count += 1
            if suggested_projects_count >= 3: # Limit to 3 projects
                break
                
    # Fallback generic project suggestion if we have missing skills but no mapping
    if suggested_projects_count < 2 and missing_skills_list:
        for skill in missing_skills_list:
            lower_skill = skill.lower()
            if lower_skill not in project_mappings:
                recommendations["project_ideas"].append(
                    f"**Project for {skill}**: Build a personal utility tool or portfolio project implementing {skill} best practices."
                )
                suggested_projects_count += 1
                if suggested_projects_count >= 3:
                    break
                    
    if not job_skills and not resume_skills:
        recommendations["project_ideas"].append(
            "Please provide a resume and job description to get specific project suggestions."
        )
    elif not missing_skills_list:
        recommendations["project_ideas"].append(
            "Since you match all skills, focus on scaling up your current projects by adding load testing, documentation, or monitoring."
        )
        
    # 4. Career Prep
    if matching_skills_list:
        skills_str = ", ".join(matching_skills_list[:3])
        recommendations["career_prep"].append(
            f"Review interview questions related to your strongest matching skills: **{skills_str}**."
        )
    recommendations["career_prep"].append(
        "Conduct mock interviews focusing on explaining technical architectures and explaining your problem-solving approaches."
    )
    if missing_skills_list:
        recommendations["career_prep"].append(
            f"Allocate time in your schedule to learn **{missing_skills_list[0]}** before applying."
        )
        
    return recommendations
