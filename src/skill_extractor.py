"""
Skill Extractor Module

This module extracts technical and soft skills from the parsed resume text
using a predefined dictionary of skills.
"""

import os
import json
import re
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Resolve path to data/skills.json relative to this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_JSON_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data", "skills.json"))

def load_skills_dictionary() -> dict:
    """
    Loads the skills dictionary from data/skills.json.
    
    Returns:
        dict: Skill categories mapped to lists of skill names.
    """
    try:
        if not os.path.exists(SKILLS_JSON_PATH):
            logger.error(f"Skills dictionary not found at {SKILLS_JSON_PATH}")
            return {}
            
        with open(SKILLS_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading skills dictionary: {str(e)}")
        return {}

def extract_skills(resume_text: str) -> dict:
    """
    Identifies and extracts skills from the resume text based on a predefined dictionary.
    Matches are case-insensitive and avoid partial word matches.
    
    Args:
        resume_text (str): The raw text extracted from the resume.
        
    Returns:
        dict: A dictionary of detected skills grouped by category.
    """
    if not resume_text:
        return {}
        
    skills_dict = load_skills_dictionary()
    detected_skills = {}
    
    for category, skills in skills_dict.items():
        category_matches = []
        for skill in skills:
            # Escape regex characters (e.g. C++ becomes C\+\+, C# becomes C\#)
            escaped_skill = re.escape(skill)
            
            # Using custom word boundary pattern that allows special characters like +, # at start/end
            # Match is successful if the skill is preceded and followed by non-alphanumeric, non-special-skill characters (or boundaries)
            pattern = rf"(?:^|[^a-zA-Z0-9_#+]){escaped_skill}(?:$|[^a-zA-Z0-9_#+])"
            
            if re.search(pattern, resume_text, re.IGNORECASE):
                category_matches.append(skill)
                
        if category_matches:
            # Deduplicate just in case, preserving order
            seen = set()
            deduped = [x for x in category_matches if not (x.lower() in seen or seen.add(x.lower()))]
            detected_skills[category] = deduped
            
    return detected_skills
