# AI-Powered Resume Builder

A Streamlit web application that helps users create professional resumes using Google's Gemini AI.

## Features

- User-friendly form interface to input resume details
- AI-powered resume content generation using Google Gemini
- PDF generation and download functionality
- Professional formatting and layout

## Application Use Cases

- **Job Seekers:** Quickly draft and generate a clean, ATS-friendly professional resume by entering minimal raw text, while letting the AI refine the phrasing and keywords.
- **Students & Graduates:** Structure academic projects and internships professionally without worrying about formatting or choosing the right action vocabularies.
- **Career Changers:** Effortlessly re-word experiences using the Gemini AI to better match new industry standards based on inputted skills.
- **Recruiters & Coaches:** Use as a tool to instantly format and standardize candidates' raw, unstructured professional histories into presentable PDF documents.

## Technologies It Uses

- **Frontend & UI:** [Streamlit](https://streamlit.io/) (for rapid interactive Python web app development)
- **AI / LLM:** [Google Gemini API](https://aistudio.google.com/) (Generative AI for rewriting bullet points, summaries, and categorizing skills)
- **PDF Generation:** [ReportLab](https://pypi.org/project/reportlab/) (for assembling the dynamic layout, fonts, and style hierarchy of the downloadable resumes)
- **Authentication:** `bcrypt` (for secure local user credential hashing and session login)
- **Data Storage:** JSON / SQLite file-based storage for basic credentials
- **Environment Management:** `python-dotenv` (for loading secure API keys)

## Setup Instructions

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file by copying `.env.example`:
   ```
   cp .env.example .env
   ```
4. Add your Google API key to the `.env` file:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   Get your API key from: https://makersuite.google.com/app/apikey

5. Run the application:
   ```
   streamlit run app.py
   ```

## How to Use

1. Fill in your personal information
2. Add your professional summary
3. Input your work experiences
4. Add your educational background
5. List your skills
6. Click "Generate Resume" to create your resume
7. Download the generated PDF

## Requirements

- Python 3.7+
- Streamlit
- Google Generative AI
- ReportLab
- python-dotenv
