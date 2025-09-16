# streamlit_app.py - Single file deployment
import streamlit as st
import PyPDF2
import docx
import io
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Page config
st.set_page_config(
    page_title="🎯 AI Resume Analyzer",
    page_icon="🎯",
    layout="wide"
)

# Cache the model to avoid reloading
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(docx_file):
    try:
        doc = docx.Document(io.BytesIO(docx_file.read()))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def calculate_fit_score(resume_text, job_description, model):
    try:
        resume_embedding = model.encode([resume_text])
        job_embedding = model.encode([job_description])
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return round(similarity * 100, 2)
    except Exception as e:
        st.error(f"Error calculating fit score: {str(e)}")
        return 0

def extract_skills(text, skill_list):
    text_lower = text.lower()
    found_skills = []
    for skill in skill_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return found_skills

# Main app
def main():
    # Header
    st.title("🎯 AI Resume Analyzer")
    st.markdown("**Analyze resume-job fit using AI**")
    
    # Load model
    with st.spinner("Loading AI model..."):
        model = load_model()
    
    # Two columns layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📄 Input")
        
        # Resume upload
        resume_file = st.file_uploader(
            "Upload Resume",
            type=['pdf', 'docx'],
            help="Upload your resume in PDF or DOCX format"
        )
        
        # Job description
        job_description = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the complete job description here..."
        )
        
        analyze_button = st.button("🔍 Analyze Match", type="primary")
    
    with col2:
        st.header("📊 Results")
        
        if analyze_button and resume_file and job_description:
            # Extract resume text
            with st.spinner("Extracting text from resume..."):
                if resume_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(resume_file)
                else:
                    resume_text = extract_text_from_docx(resume_file)
            
            if not resume_text:
                st.error("Could not extract text from resume")
                return
            
            # Calculate fit score
            with st.spinner("Analyzing compatibility..."):
                fit_score = calculate_fit_score(resume_text, job_description, model)
            
            # Display fit score
            col_score, col_gauge = st.columns([1, 1])
            
            with col_score:
                st.metric("🎯 Fit Score", f"{fit_score}%")
                
                if fit_score >= 80:
                    st.success("Excellent match!")
                elif fit_score >= 60:
                    st.warning("Good match")
                else:
                    st.error("Needs improvement")
            
            # Skills analysis
            with st.spinner("Extracting skills..."):
                common_skills = [
                    "Python", "JavaScript", "React", "Node.js", "SQL", "AWS",
                    "Docker", "Kubernetes", "Machine Learning", "Data Analysis",
                    "Project Management", "Agile", "Scrum", "Git", "Linux",
                    "Java", "C++", "HTML", "CSS", "MongoDB", "PostgreSQL",
                    "REST API", "GraphQL", "DevOps", "CI/CD", "TensorFlow",
                    "PyTorch", "Pandas", "NumPy", "Communication", "Leadership"
                ]
                
                resume_skills = extract_skills(resume_text, common_skills)
                job_skills = extract_skills(job_description, common_skills)
                
                matched_skills = list(set(resume_skills) & set(job_skills))
                missing_skills = list(set(job_skills) - set(resume_skills))
            
            # Display skills
            st.subheader("💡 Skills Analysis")
            
            skill_col1, skill_col2 = st.columns(2)
            
            with skill_col1:
                st.write("✅ **Matched Skills:**")
                if matched_skills:
                    for skill in matched_skills:
                        st.write(f"• {skill}")
                else:
                    st.write("No matching skills found")
            
            with skill_col2:
                st.write("❌ **Missing Skills:**")
                if missing_skills:
                    for skill in missing_skills:
                        st.write(f"• {skill}")
                else:
                    st.write("All required skills present")
            
            # Suggestions
            st.subheader("🚀 Improvement Suggestions")
            
            if fit_score < 60:
                st.write("🔧 **Priority Actions:**")
                st.write("• Add missing technical skills to your resume")
                st.write("• Highlight relevant experience more prominently")
                st.write("• Use keywords from the job description")
            elif fit_score < 80:
                st.write("✨ **Enhancement Tips:**")
                st.write("• Quantify your achievements with metrics")
                st.write("• Add any missing soft skills")
                st.write("• Customize resume summary for this role")
            else:
                st.write("🎉 **You're ready to apply!**")
                st.write("• Your resume aligns well with this position")
                st.write("• Consider highlighting top matching skills")
        
        elif not resume_file or not job_description:
            st.info("👆 Upload resume and paste job description to analyze")

if __name__ == "__main__":
    main()
