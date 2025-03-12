import google.generativeai as genai
import json
from config.settings import GOOGLE_API_KEY, RESUME_SECTIONS

class AIGenerator:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def enhance_experience(self, experience):
        """Enhance a single work experience entry with AI-generated improvements"""
        prompt = f"""
        Given this work experience:
        Company: {experience['company']}
        Position: {experience['position']}
        Duration: {experience['duration']}
        Responsibilities: {experience['responsibilities']}

        Please enhance this work experience by:
        1. Adding 4-5 strong, quantifiable bullet points that demonstrate achievements
        2. Using powerful action verbs at the start of each bullet
        3. Including metrics, percentages, and numbers where appropriate
        4. Highlighting leadership and initiative
        5. Incorporating relevant industry keywords
        6. Focusing on results and impact rather than just duties

        Format the response as bullet points starting with '*'.
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()
        
    def enhance_summary(self, summary, skills):
        """Generate an enhanced professional summary"""
        prompt = f"""
        Based on this professional summary:
        {summary}

        And these skills:
        {', '.join(skills)}

        Create a powerful, keyword-rich professional summary that:
        1. Highlights years of experience and key achievements
        2. Incorporates the most relevant skills naturally
        3. Shows industry expertise and unique value proposition
        4. Is written in a confident, professional tone
        5. Is 3-4 lines long and impactful
        6. Uses industry-specific terminology

        Make it compelling and ATS-friendly.
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()
        
    def enhance_skills(self, skills):
        """Organize and enhance the skills section"""
        skills_str = ', '.join(skills)
        prompt = f"""
        Given these skills:
        {skills_str}

        Please organize and enhance them by:
        1. Grouping them into relevant categories (e.g., Technical Skills, Soft Skills, Industry Knowledge)
        2. Adding any implied or related skills that would strengthen the profile
        3. Using industry-standard terminology
        4. Listing them in order of relevance
        5. Ensuring ATS-friendly formatting

        Format each category as:
        CATEGORY NAME: skill1 | skill2 | skill3
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()
        
    def enhance_education(self, education):
        """Enhance education entries with additional details"""
        enhanced_entries = []
        for edu in education:
            # Create a more detailed education entry
            enhanced_entry = {
                'institution': edu.get('institution', ''),
                'degree': edu.get('degree', ''),
                'year': edu.get('year', ''),
                'grade': edu.get('grade', ''),
                'field_of_study': edu.get('field_of_study', ''),
                'achievements': edu.get('achievements', ''),
                'location': edu.get('location', '')
            }
            enhanced_entries.append(enhanced_entry)
        return enhanced_entries

    def generate_content(self, user_info):
        """Generate the complete resume content"""
        # First, enhance individual sections
        enhanced_experiences = []
        for exp in user_info['experience']:
            enhanced_bullet_points = self.enhance_experience(exp)
            enhanced_experiences.append({
                'company': exp['company'],
                'position': exp['position'],
                'duration': exp['duration'],
                'achievements': enhanced_bullet_points
            })
            
        enhanced_summary = self.enhance_summary(user_info['summary'], user_info['skills'])
        enhanced_skills = self.enhance_skills(user_info['skills'])
        enhanced_education = self.enhance_education(user_info.get('education', []))
        
        # Create structured resume content with all personal info
        resume_content = {
            # Personal Information
            'name': user_info.get('personal_info', {}).get('name', ''),
            'email': user_info.get('personal_info', {}).get('email', ''),
            'phone': user_info.get('personal_info', {}).get('phone', ''),
            'location': user_info.get('personal_info', {}).get('location', ''),
            'linkedin': user_info.get('personal_info', {}).get('linkedin', ''),
            'website': user_info.get('personal_info', {}).get('website', ''),
            
            # Enhanced Sections
            'professional_summary': enhanced_summary,
            'experience': enhanced_experiences,
            'education': enhanced_education,
            'skills': enhanced_skills
        }
        
        return resume_content
        
    def _format_text(self, text):
        """Clean and format text for the resume"""
        # Remove any extra blank lines
        lines = [line.strip() for line in text.split('\n')]
        # Remove empty lines at the start and end
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        return '\n'.join(lines)
