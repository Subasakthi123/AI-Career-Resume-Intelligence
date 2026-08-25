"""
Resume Parser Module

This module is responsible for parsing uploaded resume files (PDF, DOCX, TXT)
and extracting raw text content.
"""

import logging
from pypdf import PdfReader

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Accepts a Streamlit uploaded PDF file, extracts text from all pages,
    combines it into one string, and handles errors/empty files gracefully.
    
    Args:
        uploaded_file (UploadedFile): Streamlit uploaded file-like object.
        
    Returns:
        str: Combined extracted text from the PDF, or empty string if extraction fails.
    """
    if uploaded_file is None:
        logger.warning("No file provided for extraction.")
        return ""
        
    extracted_text = []
    
    try:
        # pypdf's PdfReader can read file-like objects (BytesIO) directly
        reader = PdfReader(uploaded_file)
        
        # Check if the PDF has pages
        if not reader.pages:
            logger.warning("The PDF file contains no pages.")
            return ""
            
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)
            else:
                logger.debug(f"No text found on page {i + 1}.")
                
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return ""
        
    # Join page texts with newlines and strip leading/trailing spaces
    full_text = "\n".join(extracted_text).strip()
    return full_text

def parse_resume(file_path: str) -> dict:
    """
    Parses a resume file and extracts text, metadata, and structural components.
    
    Args:
        file_path (str): Path to the resume file.
        
    Returns:
        dict: A dictionary containing parsed information (e.g., raw_text, file_type, status).
    """
    # Placeholder implementation for files
    return {
        "raw_text": "",
        "file_type": "pdf" if file_path.lower().endswith(".pdf") else "unknown",
        "status": "not_implemented"
    }
