import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# PDF Settings
PDF_MARGINS = 72  # 1 inch in points
PAGE_SIZE = 'letter'

# Font Settings
FONT_SIZES = {
    'section_header': 14,
    'sub_header': 12,
    'normal_text': 10
}

# Spacing Settings
SPACING = {
    'section_after': 12,
    'sub_header_after': 6,
    'paragraph_after': 6,
    'leading': 14
}

# Resume Sections
RESUME_SECTIONS = [
    'CONTACT INFORMATION',
    'PROFESSIONAL SUMMARY',
    'WORK EXPERIENCE',
    'EDUCATION',
    'SKILLS'
]
