import streamlit as st
from src.ui_components import ResumeForm
from utils.ai_generator import AIGenerator
from utils.pdf_generator import PDFGenerator

class ResumeBuilderUI:
    def __init__(self):
        self.form = ResumeForm()
        self.ai_generator = AIGenerator()
        self.tab_titles = [
            "Personal Info",
            "Professional Summary",
            "Experience",
            "Education",
            "Skills",
            "Generate Resume"
        ]
        # Initialize active_tab in session state if not present
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0
        if 'generation_status' not in st.session_state:
            st.session_state.generation_status = ""

    def switch_tab(self, tab_index):
        st.session_state.active_tab = tab_index
        st.rerun()

    def update_progress(self, progress, status):
        """Callback to update the progress bar"""
        st.session_state.generation_progress = progress
        st.session_state.generation_status = status

    def render_pdf_preview(self, pdf_filename, resume_content):
        st.write("### Download and Preview")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Download button
            with open(pdf_filename, "rb") as file:
                st.download_button(
                    label="📥 Download Resume PDF",
                    data=file,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    key="download_resume"
                )
            
            st.write("---")
            st.write("### Resume Preview")
            try:
                from streamlit_pdf_viewer import pdf_viewer
                pdf_viewer(pdf_filename)
            except Exception:
                st.write("Resume Content Preview:")
                st.write(resume_content)

    def render_generate_section(self):
        st.header("Generate Your Resume")
        st.write("Review your information and generate your resume")
        
        # Add back button to edit information
        col1, col2, _ = st.columns([6, 2, 2])
        with col2:
            if st.button("← Back to Personal Info", key="edit_info_btn"):  
                self.switch_tab(0)  
        
        if st.button("Generate Resume", type="primary", key="generate"):
            try:
                # Get form data
                user_info = self.form.get_form_data()
                
                with st.spinner("Generating your resume..."):
                    # Generate resume content using AI
                    resume_content = self.ai_generator.generate_content(user_info)
                    
                    # Create PDF
                    pdf_filename = f"generated_resume_{st.session_state.username}.pdf"
                    pdf_gen = PDFGenerator(pdf_filename)
                    pdf_gen.generate_pdf(resume_content)
                    
                    # Show success message and download button
                    st.success("✨ Resume generated successfully!")
                    self.render_pdf_preview(pdf_filename, resume_content)
                    
            except Exception as e:
                st.error(f"An error occurred while generating the resume: {str(e)}")
                st.session_state.generation_status = "Generation failed"

    def render(self):
        st.title("AI-Powered Resume Builder")
        st.write("Fill in your details below to generate a professional resume")
        
        # Initialize active tab if not present
        if 'active_tab' not in st.session_state:
            st.session_state.active_tab = 0
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(self.tab_titles)
        
        # Personal Info tab
        with tab1:
            self.form.render_personal_info()
        
        # Professional Summary tab
        with tab2:
            self.form.render_professional_summary()
        
        # Experience tab
        with tab3:
            self.form.render_experience()
        
        # Education tab
        with tab4:
            self.form.render_education()
        
        # Skills tab
        with tab5:
            self.form.render_skills()
        
        # Generate Resume tab
        with tab6:
            self.render_generate_section()
        
        # Update tab selection using JavaScript
        if st.session_state.active_tab > 0:
            js = f"""
            <script>
                var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab-list"] [role="tab"]');
                tabs[{st.session_state.active_tab}].click();
            </script>
            """
            st.components.v1.html(js, height=0)
