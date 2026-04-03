# AI-Powered Resume Builder

A Streamlit web application that helps users create professional resumes using Google's Gemini AI.

## Features

- User-friendly form interface to input resume details
- AI-powered resume content generation using Google Gemini
- PDF generation and download functionality
- Professional formatting and layout

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
