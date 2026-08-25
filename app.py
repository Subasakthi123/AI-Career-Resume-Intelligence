import streamlit as st
from src.resume_parser import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.job_matcher import match_resume_to_job
from src.resume_scorer import calculate_resume_score
from src.ai_recommender import generate_recommendations

# Set page configuration
st.set_page_config(
    page_title="AI Career & Resume Intelligence Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_skills_grid(detected_skills: dict, theme: str = "default"):
    """
    Helper function to render skills in a beautiful badge layout.
    Themes: 'default', 'success' (matching), 'danger' (missing)
    """
    if not detected_skills:
        st.write("*No skills identified in this section.*")
        return

    if theme == "success":
        bg_color = "#1e3a2f"
        text_color = "#52c41a"
        border_color = "#27523f"
    elif theme == "danger":
        bg_color = "#3e2626"
        text_color = "#ff4d4f"
        border_color = "#5c3030"
    else: # default
        bg_color = "#2e3b4e"
        text_color = "#ffffff"
        border_color = "#4a5d78"

    for category, skills_list in detected_skills.items():
        st.markdown(f"##### **{category}** ({len(skills_list)})")
        skills_html = "".join([
            f'<span style="'
            f'background-color: {bg_color};'
            f'color: {text_color};'
            f'padding: 5px 12px;'
            f'margin: 4px;'
            f'border-radius: 20px;'
            f'display: inline-block;'
            f'font-size: 13px;'
            f'font-weight: 500;'
            f'border: 1px solid {border_color};'
            f'">{skill}</span>' 
            for skill in skills_list
        ])
        st.markdown(skills_html, unsafe_allow_html=True)
        st.write("") # Spacing between categories

def main():
    # 1. Sidebar Section
    with st.sidebar:
        st.title("AI Career & Resume Intelligence")
        st.markdown("### How It Works")
        st.write(
            "1. **Text Extraction**: The system parses the uploaded PDF resume and extracts raw text.\n"
            "2. **Skill Extraction**: Words are matched against a predefined skills dictionary (JSON) containing professional skills across 8 categories.\n"
            "3. **Skill Matching**: Compares resume skills against job description requirements to identify overlaps and gaps.\n"
            "4. **Weighted Scoring**: Evaluates profile alignment based on skill match (50%), skill coverage (25%), and resume section completeness (25%).\n"
            "5. **Career Recommendations**: Generates personalized action plans, missing section updates, and relevant project recommendations."
        )
        st.markdown("---")
        st.markdown("### Technologies Used")
        st.write(
            "- **Streamlit**: Web Application Interface\n"
            "- **pypdf**: PDF Text Extraction\n"
            "- **Python Re**: Case-Insensitive Regex Parsing\n"
            "- **JSON**: Structured Skills Dictionary"
        )

    # 2. Main Header & Subtitle
    st.title("AI Career & Resume Intelligence Platform 💼")
    st.markdown(
        "##### Analyze your resume, compare it with a target job, identify skill gaps, and get actionable career recommendations."
    )
    
    # 3. User instructions
    st.info("Upload your resume and paste a target job description to begin analysis.")
    st.markdown("---")

    # 4. Input Section (Resume & Job Description)
    input_col1, input_col2 = st.columns([1, 1])

    # Session states for values
    if "extracted_resume_text" not in st.session_state:
        st.session_state.extracted_resume_text = ""
    if "resume_skills" not in st.session_state:
        st.session_state.resume_skills = {}

    with input_col1:
        st.subheader("Section 1 — Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF resume file", 
            type=["pdf"],
            help="Only PDF files are supported at this stage.",
            key="resume_uploader"
        )

        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                extracted_text = extract_text_from_pdf(uploaded_file)
                st.session_state.extracted_resume_text = extracted_text
                
            if st.session_state.extracted_resume_text:
                st.success("Successfully extracted text from the PDF resume!")
                # Parse resume skills immediately
                detected_skills = extract_skills(st.session_state.extracted_resume_text)
                st.session_state.resume_skills = detected_skills
                
                with st.expander("Show Extracted Resume Text", expanded=False):
                    st.text_area(
                        label="Raw Resume Text",
                        value=st.session_state.extracted_resume_text,
                        height=200,
                        disabled=True,
                        label_visibility="collapsed"
                    )
            else:
                st.error(
                    "Could not extract text from the PDF. The file may be empty, "
                    "scanned (image-only), or corrupted."
                )
        else:
            st.session_state.extracted_resume_text = ""
            st.session_state.resume_skills = {}

    with input_col2:
        st.subheader("Section 2 — Target Job Description")
        job_desc = st.text_area(
            "Paste target job description here to compare",
            height=265,
            placeholder="We are looking for a Software Engineer with strong experience in Python, SQL, and Machine Learning. The ideal candidate has worked with AWS, Git, and Docker...",
            key="job_desc_input"
        )

    # 5. Output Results Workflow (Visible when both inputs are provided)
    has_resume = bool(st.session_state.extracted_resume_text)
    has_job = bool(job_desc.strip())

    if has_resume and has_job:
        # Run matching
        detected_job_skills = extract_skills(job_desc)
        match_result = match_resume_to_job(st.session_state.resume_skills, detected_job_skills)
        
        # Run scoring
        score_result = calculate_resume_score(
            st.session_state.extracted_resume_text,
            st.session_state.resume_skills,
            detected_job_skills,
            match_result
        )
        
        # Run recommendations
        recs = generate_recommendations(
            st.session_state.extracted_resume_text,
            st.session_state.resume_skills,
            detected_job_skills,
            match_result,
            score_result
        )

        st.markdown("---")

        # Section 6: Resume Analysis Score
        st.subheader("Section 6 — Resume Analysis Score")
        score_col1, score_col2, score_col3, score_col4 = st.columns(4)
        
        with score_col1:
            st.metric(
                label="Overall Score", 
                value=f"{score_result['overall_score']}/100"
            )
        with score_col2:
            st.metric(
                label="Job Skill Match (50% Weight)", 
                value=f"{score_result['job_match_score']}%"
            )
        with score_col3:
            st.metric(
                label="Skill Coverage (25% Weight)", 
                value=f"{score_result['skill_coverage_score']}%"
            )
        with score_col4:
            st.metric(
                label="Content Quality (25% Weight)", 
                value=f"{score_result['content_quality_score']}%"
            )
            
        st.progress(score_result["overall_score"] / 100.0)
        
        sections_str = ", ".join(score_result["detected_sections"]) if score_result["detected_sections"] else "None"
        st.markdown(f"**Detected Resume Sections:** *{sections_str}*")
        st.caption("ℹ️ *This is an application-generated analysis score, not an official ATS or recruiter score.*")
        
        st.markdown("---")

        # Section 5: Job Match Analysis
        st.subheader("Section 5 — Job Match Analysis")
        match_col1, match_col2 = st.columns(2)
        
        with match_col1:
            st.markdown(f"##### **✅ Matching Skills** ({match_result['total_matched_skills']})")
            if match_result["matching_skills"]:
                render_skills_grid(match_result["matching_skills"], theme="success")
            else:
                st.info("No matching skills found between the resume and the job description.")
                
        with match_col2:
            missing_count = match_result["total_job_skills"] - match_result["total_matched_skills"]
            st.markdown(f"##### **❌ Missing Required Skills** ({missing_count})")
            if match_result["missing_skills"]:
                render_skills_grid(match_result["missing_skills"], theme="danger")
            else:
                st.success("Perfect match! The resume contains all the required skills for the job description.")

        st.markdown("---")

        # Sections 3 & 4: Detailed Skill Profiles (in expandable tabs)
        with st.expander("Show Detailed Categorized Skills (Sections 3 & 4)", expanded=False):
            skills_col1, skills_col2 = st.columns(2)
            with skills_col1:
                st.markdown("#### **Section 3 — Resume Skills**")
                if st.session_state.resume_skills:
                    render_skills_grid(st.session_state.resume_skills)
                else:
                    st.info("No predefined skills detected in the resume.")
            with skills_col2:
                st.markdown("#### **Section 4 — Job Requirements**")
                if detected_job_skills:
                    render_skills_grid(detected_job_skills)
                else:
                    st.info("No predefined skills detected in the job description.")

        st.markdown("---")

        # Section 7: AI Career Recommendations
        st.subheader("Section 7 — AI Career Recommendations")
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("#### **🛠️ Skills to Acquire**")
            for item in recs["skills_to_learn"]:
                st.markdown(f"- {item}")
            st.write("")
            
            st.markdown("#### **🚀 Portfolio Project Ideas**")
            for item in recs["project_ideas"]:
                st.markdown(f"- {item}")
        
        with rec_col2:
            st.markdown("#### **📝 Resume Improvements**")
            for item in recs["resume_improvements"]:
                st.markdown(f"- {item}")
            st.write("")
            
            st.markdown("#### **💼 Career & Interview Preparation**")
            for item in recs["career_prep"]:
                st.markdown(f"- {item}")
                
        st.warning(
            "⚠️ *Disclaimer: These are application-generated recommendations based on automated resume parsing "
            "and keyword matching. They are intended for guidance and self-improvement purposes only and do not "
            "constitute professional career coaching or employment advice.*"
        )
        
    else:
        # Prompt user if input is missing
        st.markdown("---")
        st.warning("⚠️ **Awaiting Inputs**: Please make sure you upload a resume PDF and enter a target job description to view the analysis reports.")

if __name__ == "__main__":
    main()
