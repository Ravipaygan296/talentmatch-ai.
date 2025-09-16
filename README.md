# 🚀 AI Resume Analyzer - Complete Setup Guide

## 🎯 Features
- **100% Free** - Uses local Hugging Face models (no API keys needed!)
- **Smart Analysis** - Embedding-based similarity scoring
- **Skill Extraction** - Automatically finds matched/missing skills
- **HR Summary** - AI-generated professional assessment
- **Market Insights** - Salary ranges and industry trends
- **Modern UI** - Beautiful React + Tailwind interface

## 📋 Prerequisites
- Python 3.9+ 
- Node.js 16+
- 4GB+ RAM (for model loading)
- GPU optional (faster inference)

## 🏗️ Project Structure
```
ai-resume-analyzer/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── docker-compose.yml
└── README.md
```

## ⚡ Quick Start (Local Development)

### 1. Backend Setup
```bash
# Create project directory
mkdir ai-resume-analyzer
cd ai-resume-analyzer
mkdir backend frontend

# Setup Python virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend (will download models on first run)
python main.py
```

### 2. Frontend Setup
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🐳 Docker Setup (Recommended)

### 1. Create Project Files
Create all the files from the artifacts above in your project directory.

### 2. Build and Run
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d
```

### 3. Stop Services
```bash
docker-compose down
```

## 📁 File Creation Checklist

Create these files in your project:

**Backend Files:**
- [ ] `backend/main.py` (FastAPI application)
- [ ] `backend/requirements.txt` (Python dependencies)
- [ ] `backend/Dockerfile` (Docker configuration)

**Frontend Files:**
- [ ] `frontend/src/App.js` (React component)
- [ ] `frontend/src/index.js` (React entry point)
- [ ] `frontend/package.json` (Node.js dependencies)
- [ ] `frontend/tailwind.config.js` (Tailwind configuration)

**Root Files:**
- [ ] `docker-compose.yml` (Multi-service configuration)
- [ ] `README.md` (This guide)

## 🧠 Model Information

### Loaded Models (First Run):
1. **sentence-transformers/all-MiniLM-L6-v2** (~90MB)
   - Purpose: Resume-job similarity scoring
   - Speed: Fast inference

2. **facebook/bart-large-cnn** (~1.2GB)
   - Purpose: HR summary generation
   - Speed: Moderate

3. **dbmdz/bert-large-cased-finetuned-conll03-english** (~1.3GB)
   - Purpose: Named Entity Recognition (skill extraction)
   - Speed: Fast

**Total Download**: ~2.6GB (one-time download)

## 🎮 Usage Guide

### 1. Upload Resume
- Click upload area or drag & drop
- Supported formats: PDF, DOCX, TXT
- Or paste text directly

### 2. Add Job Description
- Copy job posting content
- Paste into text area

### 3. Analyze Match
- Click "Analyze Match" button
- Wait 10-30 seconds for AI processing
- View comprehensive results

### 4. Interpret Results
- **Fit Score**: Overall compatibility (0-100%)
- **Matched Skills**: Skills found in both resume and job
- **Missing Skills**: Required skills not in resume
- **HR Summary**: Professional assessment
- **Market Insights**: Industry data and trends
- **Suggestions**: Actionable improvement tips

## 🔧 Customization Options

### Add More Skills Patterns
Edit `main.py` skill extraction patterns:
```python
skill_patterns = [
    r'\b(?:Python|Java|JavaScript|TypeScript)\b',
    r'\b(?:React|Angular|Vue|Django)\b',
    # Add your industry-specific patterns
]
```

### Modify UI Colors
Edit `App.js` Tailwind classes:
```javascript
// Change primary colors
from-indigo-600 to-purple-600  // Main gradient
text-indigo-600                // Accent color
```

### Switch Models
Replace model names in `main.py`:
```python
# For different embedding model:
self.embedding_model = SentenceTransformer('all-mpnet-base-v2')

# For different summarizer:
self.summarizer = pipeline("summarization", model="t5-small")
```

## 🚨 Troubleshooting

### Backend Issues:
**Model Download Fails:**
```bash
# Clear cache and retry
pip cache purge
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Out of Memory:**
- Reduce batch size in model loading
- Use smaller models (t5-small instead of bart-large-cnn)
- Close other applications

**Import Errors:**
```bash
# Reinstall with force
pip install --force-reinstall transformers sentence-transformers
```

### Frontend Issues:
**Tailwind Not Working:**
```bash
# Install and configure Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**CORS Errors:**
- Check backend CORS middleware is enabled
- Verify frontend proxy in package.json

**Connection Refused:**
- Ensure backend is running on port 8000
- Check firewall settings

## 🔮 Future Enhancements

### Phase 2 Features:
- [ ] **Multi-language Support** (Spanish, French, etc.)
- [ ] **Industry-Specific Analysis** (Tech, Healthcare, Finance)
- [ ] **Resume Improvement Suggestions** with examples
- [ ] **ATS Compatibility Checker**
- [ ] **Salary Prediction Model**
- [ ] **LinkedIn Profile Analysis**

### Phase 3 Features:
- [ ] **Interview Question Generator**
- [ ] **Cover Letter Generator**
- [ ] **Career Path Recommendations**
- [ ] **Skills Gap Learning Resources**
- [ ] **Real-time Market Data Integration**

## 💡 Performance Tips

### Optimize Loading Time:
1. **Pre-download Models**: Uncomment Docker model download lines
2. **Use GPU**: Install CUDA for faster inference
3. **Smaller Models**: Use distilled versions for faster processing
4. **Caching**: Implement Redis for repeated analyses

### Production Deployment:
1. **Use Gunicorn**: Replace Uvicorn for production
2. **Add Load Balancer**: Nginx for static files
3. **Database**: PostgreSQL for user data
4. **Authentication**: JWT tokens for user sessions

## 🤝 Contributing

### Development Setup:
```bash
# Fork repository
git clone https://github.com/yourusername/ai-resume-analyzer
cd ai-resume-analyzer

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git commit -m "Add your feature"

# Push and create pull request
git push origin feature/your-feature-name
```

### Code Style:
- **Python**: Black formatter, flake8 linting
- **JavaScript**: Prettier, ESLint
- **Commits**: Conventional commit messages

## 📄 License

MIT License - Feel free to use for personal and commercial projects!

## 🆘 Support

**Need help?**
1. Check this README first
2. Search existing GitHub issues
3. Create new issue with:
   - Error message
   - Steps to reproduce
   - System info (OS, Python version)

---

**Built with ❤️ using Hugging Face Transformers, FastAPI, and React**

*Happy job hunting! 🎯*
