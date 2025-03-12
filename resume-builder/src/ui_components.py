import streamlit as st

class ResumeForm:
    def __init__(self):
        self.personal_info = {}
        self.experiences = []
        self.education = []
        self.skills = ""
        self.summary = ""
        if 'phone_number' not in st.session_state:
            st.session_state.phone_number = ""
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0
        if 'last_valid_phone' not in st.session_state:
            st.session_state.last_valid_phone = ""
        if 'professional_summary' not in st.session_state:
            st.session_state.professional_summary = ""

    def validate_indian_phone(self, number):
        import re
        # Check if it's a valid Indian mobile number
        pattern = r'^[6-9][0-9]{9}$'
        return bool(re.match(pattern, number))

    def check_and_switch_tab(self, current_tab):
        """Helper function to switch to next tab"""
        st.session_state.active_tab = current_tab + 1
        st.rerun()

    def render_next_button(self, current_tab, is_valid=True):
        """Render next and back buttons that switch tabs"""
        col1, col2, col3 = st.columns([6, 1, 1])
        
        # Only show back button if not on first tab
        if current_tab > 0:
            with col2:
                if st.button("← Back", key=f"back_btn_{current_tab}"):
                    st.session_state.active_tab = current_tab - 1
                    st.rerun()
        
        with col3:
            if st.button("Next →", key=f"next_btn_{current_tab}", disabled=not is_valid):
                self.check_and_switch_tab(current_tab)

    def render_personal_info(self):
        st.header("Personal Information")
        
        # Basic info in two columns
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", key="name_input")
            email = st.text_input("Email", key="email_input")
            location = st.text_input("Location", key="location_input")
        with col2:
            phone_input = st.text_input(
                "Phone Number",
                value=st.session_state.get('phone_number', ''),
                max_chars=10,
                help="Enter a valid 10-digit Indian mobile number (starting with 6-9)",
                key="phone_input_field"
            )
        
        # Professional profiles section
        st.subheader("Professional Profiles")
        col3, col4 = st.columns(2)
        with col3:
            linkedin = st.text_input(
                "LinkedIn Profile",
                help="Enter your LinkedIn profile URL",
                placeholder="https://linkedin.com/in/username",
                key="linkedin_input"
            )
            github = st.text_input(
                "GitHub Profile",
                help="Enter your GitHub profile URL",
                placeholder="https://github.com/username",
                key="github_input"
            )
        with col4:
            website = st.text_input(
                "Personal Website",
                help="Enter your personal website URL",
                placeholder="https://example.com",
                key="website_input"
            )

        # Process phone input and validate all fields
        is_valid = False
        if phone_input and name and email and location:
            digits_only = ''.join(filter(str.isdigit, phone_input))
            
            if digits_only != phone_input:
                st.session_state.phone_number = digits_only
                st.rerun()
            
            if self.validate_indian_phone(digits_only):
                # Store all personal info including professional profiles
                self.personal_info = {
                    "name": name,
                    "email": email,
                    "location": location,
                    "phone": digits_only,
                    "linkedin": linkedin if linkedin else "",
                    "github": github if github else "",
                    "website": website if website else ""
                }
                st.success("✓ All required fields complete")
                is_valid = True
            else:
                st.error("Please enter a valid phone number")
        
        self.render_next_button(0, is_valid)

    def render_professional_summary(self):
        st.header("Professional Summary")
        summary = st.text_area(
            "Brief professional summary about yourself",
            value=st.session_state.professional_summary,  # Load from session state
            key="summary_input",
            height=150
        )
        
        is_valid = False
        if summary and len(summary.strip()) > 0:
            self.summary = summary
            st.session_state.professional_summary = summary  # Save to session state
            st.success("✓ Summary complete")
            is_valid = True
        
        self.render_next_button(1, is_valid)

    def render_experience(self):
        st.header("Work Experience")
        num_experiences = st.number_input(
            "Number of work experiences",
            min_value=0,
            max_value=10,
            value=0,
            key="num_exp"
        )
        
        experiences = []
        all_fields_filled = True
        
        for i in range(num_experiences):
            st.subheader(f"Experience {i+1}")
            col1, col2 = st.columns(2)
            with col1:
                company = st.text_input(f"Company Name #{i+1}", key=f"company_{i}")
                position = st.text_input(f"Position #{i+1}", key=f"position_{i}")
            with col2:
                duration = st.text_input(f"Duration #{i+1} (e.g., 2020-2022)", key=f"duration_{i}")
            responsibilities = st.text_area(f"Key Responsibilities #{i+1}", key=f"resp_{i}")
            
            if not all([company, position, duration, responsibilities]):
                all_fields_filled = False
            
            exp = {
                "company": company,
                "position": position,
                "duration": duration,
                "responsibilities": responsibilities
            }
            experiences.append(exp)
        
        is_valid = True
        if num_experiences > 0:
            if all_fields_filled and experiences:
                st.success("✓ Experience details complete")
            else:
                is_valid = False
                
        self.experiences = experiences
        self.render_next_button(2, is_valid)

    def render_education(self):
        st.header("Education")
        num_education = st.number_input(
            "Number of educational qualifications",
            min_value=0,
            max_value=5,
            value=0,
            key="num_edu"
        )
        
        education = []
        all_fields_filled = True
        
        for i in range(num_education):
            st.subheader(f"Education {i+1}")
            col1, col2 = st.columns(2)
            with col1:
                institution = st.text_input(f"Institution Name #{i+1}", key=f"inst_{i}")
                degree = st.text_input(f"Degree #{i+1}", key=f"degree_{i}")
            with col2:
                year = st.text_input(f"Year #{i+1}", key=f"year_{i}")
                grade = st.text_input(f"Grade/CGPA #{i+1} (optional)", key=f"grade_{i}")
            
            if not all([institution, degree, year]):
                all_fields_filled = False
            
            edu = {
                "institution": institution,
                "degree": degree,
                "year": year,
                "grade": grade
            }
            education.append(edu)
        
        is_valid = True
        if num_education > 0:
            if all_fields_filled and education:
                st.success("✓ Education details complete")
            else:
                is_valid = False
                
        self.education = education
        self.render_next_button(3, is_valid)

    def render_skills(self):
        st.header("Skills")
        skills = st.text_area(
            "List your key skills (one per line)",
            height=150,
            key="skills_input"
        )
        
        is_valid = False
        if skills and len(skills.strip()) > 0:
            self.skills = skills
            st.success("✓ Skills complete")
            is_valid = True
        
        self.render_next_button(4, is_valid)

    def handle_phone_change(self):
        # Get the current phone input
        phone_input = st.session_state.phone_input_field
        
        # If it's a valid phone number, move to the next tab
        if phone_input and self.validate_indian_phone(phone_input):
            st.session_state.active_tab = 1

    def get_form_data(self):
        return {
            "personal_info": self.personal_info,
            "summary": st.session_state.get('professional_summary', ''),  # Get from session state
            "experience": self.experiences,
            "education": self.education,
            "skills": self.skills.split('\n') if self.skills else []
        }
