# main.py - Enhanced FastAPI Backend with Hugging Face LLMs
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional, List, Dict
import json

# Hugging Face imports
from transformers import pipeline, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Document processing
import PyPDF2
import docx
import io
import re

app = FastAPI(title="AI Resume Analyzer", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instances (loaded once at startup)
class ModelManager:
    def __init__(self):
        print("🔄 Loading Hugging Face models...")
        
        # Embedding model for similarity scoring
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Summarization model
        self.summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Text generation for insights
        self.text_generator = pipeline(
            "text-generation",
            model="microsoft/DialoGPT-small",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # NER for skill extraction
        self.ner_pipeline = pipeline(
            "ner",
            model="dbmdz/bert-large-cased-finetuned-conll03-english",
            aggregation_strategy="simple"
        )
        
        print("✅ All models loaded successfully!")

# Initialize models at startup
models = ModelManager()

# Pydantic models
class JobAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str
    use_api: Optional[bool] = False  # Toggle between local/API inference

class AnalysisResponse(BaseModel):
    fit_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    hr_summary: str
    market_insights: Dict[str, str]
    improvement_suggestions: List[str]

# Utility functions
def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading DOCX: {str(e)}")

def extract_skills_from_text(text: str) -> List[str]:
    """Extract skills using NER and predefined skill patterns"""
    
    # Common technical skills patterns
    skill_patterns = [
        r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|Ruby|PHP|Go|Rust|Swift|Kotlin)\b',
        r'\b(?:React|Angular|Vue|Node\.js|Django|Flask|Spring|Laravel|Express)\b',
        r'\b(?:AWS|Azure|GCP|Docker|Kubernetes|Jenkins|Git|Linux|Windows)\b',
        r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Oracle|SQLite)\b',
        r'\b(?:HTML|CSS|SASS|Bootstrap|Tailwind|jQuery|REST|GraphQL|API)\b',
        r'\b(?:Machine Learning|Deep Learning|AI|Data Science|NLP|Computer Vision)\b',
        r'\b(?:Agile|Scrum|DevOps|CI/CD|TDD|Microservices|Blockchain)\b'
    ]
    
    skills = set()
    
    # Extract using regex patterns
    for pattern in skill_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            skills.add(match.group().strip())
    
    # Extract using NER (for additional entities)
    try:
        entities = models.ner_pipeline(text)
        for entity in entities:
            if entity['entity_group'] in ['MISC', 'ORG'] and len(entity['word']) > 2:
                skills.add(entity['word'])
    except:
        pass  # Fallback if NER fails
    
    return list(skills)

def calculate_fit_score(resume_text: str, job_description: str) -> float:
    """Calculate similarity score using sentence embeddings"""
    try:
        # Generate embeddings
        resume_embedding = models.embedding_model.encode([resume_text])
        job_embedding = models.embedding_model.encode([job_description])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        
        # Convert to percentage and ensure it's between 0-100
        fit_score = max(0, min(100, similarity * 100))
        
        return round(fit_score, 2)
    except Exception as e:
        print(f"Error calculating fit score: {e}")
        return 0.0

def generate_hr_summary(resume_text: str, job_description: str, fit_score: float) -> str:
    """Generate HR summary using summarization model"""
    try:
        # Create input text for summarization
        input_text = f"""
        Job Match Analysis:
        Fit Score: {fit_score}%
        
        Resume Summary: {resume_text[:500]}...
        
        Job Requirements: {job_description[:500]}...
        
        Please provide a professional HR summary of this candidate's suitability.
        """
        
        # Truncate if too long for model
        if len(input_text) > 1024:
            input_text = input_text[:1024]
        
        summary = models.summarizer(input_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
        
    except Exception as e:
        print(f"Error generating HR summary: {e}")
        # Fallback summary
        if fit_score >= 80:
            return f"Excellent candidate with {fit_score}% compatibility. Strong alignment with job requirements."
        elif fit_score >= 60:
            return f"Good candidate with {fit_score}% compatibility. Meets most job requirements with some gaps."
        elif fit_score >= 40:
            return f"Moderate fit with {fit_score}% compatibility. Some relevant experience but significant gaps exist."
        else:
            return f"Limited fit with {fit_score}% compatibility. Major skill gaps need to be addressed."

def get_market_insights(matched_skills: List[str], missing_skills: List[str]) -> Dict[str, str]:
    """Generate market insights (simulated for now)"""
    insights = {
        "salary_range": "$60,000 - $120,000",
        "demand_level": "High" if len(matched_skills) > 5 else "Moderate",
        "growth_trend": "Growing 15% year-over-year",
        "top_locations": "San Francisco, New York, Austin, Seattle",
        "skill_priority": missing_skills[0] if missing_skills else "Continue developing current skills"
    }
    return insights

def generate_improvement_suggestions(missing_skills: List[str], fit_score: float) -> List[str]:
    """Generate personalized improvement suggestions"""
    suggestions = []
    
    if fit_score < 60:
        suggestions.append("Consider taking online courses to fill critical skill gaps")
        suggestions.append("Update resume to better highlight relevant experience")
    
    if missing_skills:
        suggestions.append(f"Focus on learning: {', '.join(missing_skills[:3])}")
        suggestions.append("Build portfolio projects demonstrating these skills")
    
    if fit_score >= 70:
        suggestions.append("Your profile is strong - consider applying confidently")
        suggestions.append("Prepare for interviews focusing on your key strengths")
    
    suggestions.append("Network with professionals in this field")
    suggestions.append("Keep resume updated with latest projects and achievements")
    
    return suggestions

# API Routes
@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer API v2.0 - Powered by Hugging Face 🤗"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": True,
        "gpu_available": torch.cuda.is_available()
    }

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and extract text from resume file"""
    
    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported")
    
    try:
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(content)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(content)
        else:  # text/plain
            text = content.decode('utf-8')
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        return {
            "filename": file.filename,
            "text": text,
            "word_count": len(text.split()),
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_job_match(request: JobAnalysisRequest):
    """Analyze job match between resume and job description"""
    
    try:
        print(f"🔍 Analyzing job match...")
        
        # Extract skills from both texts
        resume_skills = extract_skills_from_text(request.resume_text)
        job_skills = extract_skills_from_text(request.job_description)
        
        print(f"📝 Resume skills found: {len(resume_skills)}")
        print(f"💼 Job skills found: {len(job_skills)}")
        
        # Find matched and missing skills
        matched_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))
        
        # Calculate fit score
        fit_score = calculate_fit_score(request.resume_text, request.job_description)
        print(f"📊 Fit score calculated: {fit_score}%")
        
        # Generate HR summary
        hr_summary = generate_hr_summary(request.resume_text, request.job_description, fit_score)
        
        # Get market insights
        market_insights = get_market_insights(matched_skills, missing_skills)
        
        # Generate improvement suggestions
        improvement_suggestions = generate_improvement_suggestions(missing_skills, fit_score)
        
        return AnalysisResponse(
            fit_score=fit_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            hr_summary=hr_summary,
            market_insights=market_insights,
            improvement_suggestions=improvement_suggestions
        )
        
    except Exception as e:
        print(f"❌ Error in analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting AI Resume Analyzer...")
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )