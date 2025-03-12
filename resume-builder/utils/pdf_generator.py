from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

class PDFGenerator:
    def __init__(self, output_file):
        self.output_file = output_file
        self.width, self.height = letter
        
        # Register custom fonts
        font_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts')
        os.makedirs(font_dir, exist_ok=True)
        
        # Modern color scheme
        self.colors = {
            'primary': colors.HexColor('#1A237E'),  # Dark blue - more professional
            'secondary': colors.HexColor('#0D47A1'),  # Medium blue
            'accent': colors.HexColor('#1565C0'),  # Light blue - less aggressive than red
            'text': colors.HexColor('#212121'),  # Near black - better readability
            'subtext': colors.HexColor('#424242')  # Darker gray - improved contrast
        }
        
        # Define styles
        self.styles = getSampleStyleSheet()
        self.define_styles()
        
    def define_styles(self):
        """Define custom styles for the resume"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='ResumeHeader',
            fontSize=28,
            leading=34,
            textColor=self.colors['primary'],
            spaceAfter=12,
            spaceBefore=24,
            fontName='Helvetica-Bold',
            alignment=1  # Center alignment
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='ResumeSectionHeader',
            fontSize=18,
            leading=22,
            textColor=self.colors['secondary'],
            spaceAfter=4,
            spaceBefore=16,
            fontName='Helvetica-Bold'
        ))

        # Add new styles for better content hierarchy
        self.styles.add(ParagraphStyle(
            name='ResumeSubHeader',
            fontSize=14,
            leading=18,
            textColor=self.colors['primary'],
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='ResumeBody',
            fontSize=12,
            leading=16,
            textColor=self.colors['text'],
            spaceAfter=8,
            fontName='Helvetica',
            bulletIndent=20,
            leftIndent=20
        ))

        self.styles.add(ParagraphStyle(
            name='ResumeMetadata',
            fontSize=11,
            leading=14,
            textColor=self.colors['subtext'],
            spaceAfter=4,
            fontName='Helvetica-Oblique'
        ))

        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['ResumeMetadata'],
            alignment=1,  # Center alignment
            spaceBefore=4,
            spaceAfter=4
        ))

        # Add style for social media links
        self.styles.add(ParagraphStyle(
            name='SocialLinks',
            fontSize=12,
            leading=16,
            textColor=self.colors['primary'],
            spaceAfter=2,
            spaceBefore=2,
            fontName='Helvetica',
            alignment=1,  # Center alignment
            linkUnderline=False  # No underline for cleaner look
        ))
        
    def create_social_links(self, linkedin_url=None, github_url=None):
        """Create social media links"""
        social_elements = []
        
        if linkedin_url:
            social_elements.append(
                Paragraph(
                    f'<link href="{linkedin_url}"><font color="#0077B5">🔗 LinkedIn</font></link>',
                    self.styles['SocialLinks']
                )
            )
        
        if github_url:
            social_elements.append(
                Paragraph(
                    f'<link href="{github_url}"><font color="#333333">⌘ GitHub</font></link>',
                    self.styles['SocialLinks']
                )
            )
        
        return social_elements

    def add_section_header(self, story, text):
        """Add a section header with an underline"""
        story.append(Paragraph(text, self.styles['ResumeSectionHeader']))
        story.append(HRFlowable(
            width="100%",
            thickness=1,
            color=self.colors['secondary'],
            spaceBefore=0,
            spaceAfter=8,
            lineCap='round'
        ))
        
    def create_bullet_list(self, items):
        """Create a bullet point list"""
        bullets = []
        for item in items:
            if item.strip():
                bullet = ListItem(
                    Paragraph(item.strip(), self.styles['ResumeBody']),
                    leftIndent=20,
                    bulletColor=self.colors['accent']
                )
                bullets.append(bullet)
        return ListFlowable(
            bullets,
            bulletType='bullet',
            start='•'
        )
        
    def generate_pdf(self, resume_content):
        """Generate a PDF resume from the given content"""
        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Add name as main header
        name = resume_content.get('name', '').strip()
        if name:
            story.append(Paragraph(name, self.styles['ResumeHeader']))
        
        # Add contact info in a clean format
        contact_info = []
        
        # Add email and phone in first line
        primary_contact = []
        if resume_content.get('email'):
            primary_contact.append(f"Email: {resume_content['email']}")
        if resume_content.get('phone'):
            primary_contact.append(f"Phone: {resume_content['phone']}")
        if primary_contact:
            story.append(Paragraph(
                ' | '.join(primary_contact),
                self.styles['ContactInfo']
            ))
            
        # Add location
        if resume_content.get('location'):
            story.append(Paragraph(
                f"Location: {resume_content['location']}",
                self.styles['ContactInfo']
            ))
        
        # Add social media links with icons
        social_elements = self.create_social_links(
            linkedin_url=resume_content.get('linkedin'),
            github_url=resume_content.get('github')
        )
        
        if social_elements:
            # Create a table for social links to keep them centered and properly spaced
            social_data = [[element] for element in social_elements]
            social_table = Table(social_data, colWidths=[doc.width * 0.8])
            social_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ]))
            story.append(social_table)
        
        story.append(Spacer(1, 0.2*inch))
        
        # Add professional summary
        if resume_content.get('professional_summary'):
            self.add_section_header(story, 'Professional Summary')
            story.append(Paragraph(resume_content['professional_summary'], self.styles['ResumeBody']))
            story.append(Spacer(1, 0.2*inch))
        
        # Add experience section with enhanced formatting
        if resume_content.get('experience'):
            self.add_section_header(story, 'Professional Experience')
            for exp in resume_content['experience']:
                # Company and position as sub-header
                story.append(Paragraph(
                    f"{exp.get('company', '')} - {exp.get('position', '')}",
                    self.styles['ResumeSubHeader']
                ))
                
                # Duration as metadata
                if exp.get('duration'):
                    story.append(Paragraph(
                        exp['duration'],
                        self.styles['ResumeMetadata']
                    ))
                
                # Achievements as bullet points
                achievements = exp.get('achievements', '').split('\n')
                bullets = []
                for achievement in achievements:
                    if achievement.strip():
                        # Remove the asterisk if it exists at the start
                        achievement = achievement.strip().lstrip('*').strip()
                        bullets.append(ListItem(
                            Paragraph(achievement, self.styles['ResumeBody']),
                            bulletColor=self.colors['accent']
                        ))
                if bullets:
                    story.append(ListFlowable(
                        bullets,
                        bulletType='bullet',
                        leftIndent=20,
                        bulletFontSize=8
                    ))
                story.append(Spacer(1, 0.15*inch))
        
        # Add education section with enhanced formatting
        if resume_content.get('education'):
            self.add_section_header(story, 'Education')
            for edu in resume_content['education']:
                # Institution and degree
                header_parts = []
                if edu.get('institution'):
                    header_parts.append(edu['institution'])
                if edu.get('degree'):
                    header_parts.append(edu['degree'])
                if edu.get('field_of_study'):
                    header_parts.append(edu['field_of_study'])
                
                if header_parts:
                    story.append(Paragraph(
                        ' - '.join(header_parts),
                        self.styles['ResumeSubHeader']
                    ))
                
                # Education details
                details = []
                if edu.get('year'):
                    details.append(edu['year'])
                if edu.get('grade'):
                    details.append(f"Grade: {edu['grade']}")
                if edu.get('location'):
                    details.append(edu['location'])
                
                if details:
                    story.append(Paragraph(
                        ' | '.join(details),
                        self.styles['ResumeMetadata']
                    ))
                
                # Add achievements if any
                if edu.get('achievements'):
                    achievements = edu['achievements'].split('\n')
                    bullets = []
                    for achievement in achievements:
                        if achievement.strip():
                            bullets.append(ListItem(
                                Paragraph(achievement.strip(), self.styles['ResumeBody']),
                                bulletColor=self.colors['accent']
                            ))
                    if bullets:
                        story.append(ListFlowable(
                            bullets,
                            bulletType='bullet',
                            leftIndent=20,
                            bulletFontSize=8
                        ))
                
                story.append(Spacer(1, 0.15*inch))
        
        # Add skills section
        if resume_content.get('skills'):
            self.add_section_header(story, 'Skills')
            story.append(Paragraph(resume_content['skills'], self.styles['ResumeBody']))
        
        # Generate the PDF
        doc.build(story)
