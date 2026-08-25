# AI-Career-Resume-Intelligence

An AI-powered Resume and Job Matching web application built with Streamlit.

## Project Structure

```text
AI-Career-Resume-Intelligence/
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore file
├── src/                    # Source code directory
│   ├── resume_parser.py    # Extracts text and structure from resumes
│   ├── skill_extractor.py  # Identifies and categorizes skills
│   ├── job_matcher.py      # Matches resumes with job descriptions
│   ├── resume_scorer.py    # Scores resumes against job requirements
│   ├── ai_recommender.py   # Generates career and resume improvement recommendations
│   └── database.py         # Mock or local database handler
├── data/                   # Data directory for storing uploaded/processed resumes and jobs
└── assets/                 # Assets directory for images, styles, and other static files
```

## Getting Started

1. Clone or download the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
