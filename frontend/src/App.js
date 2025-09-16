import React, { useState, useRef } from 'react';
import { Upload, FileText, Briefcase, TrendingUp, Target, Star, CheckCircle, AlertCircle, Brain, Zap } from 'lucide-react';

const ResumeAnalyzer = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploadLoading(true);
    setResumeFile(file);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload-resume', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResumeText(data.text);
      } else {
        alert('Error uploading file. Please try again.');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading file. Please check your connection.');
    } finally {
      setUploadLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!resumeText.trim() || !jobDescription.trim()) {
      alert('Please provide both resume text and job description.');
      return;
    }

    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
          use_api: false // Using local inference
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysis(data);
      } else {
        alert('Analysis failed. Please try again.');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Analysis failed. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const getFitScoreColor = (score) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-yellow-500';
    if (score >= 40) return 'text-orange-500';
    return 'text-red-500';
  };

  const getFitScoreGradient = (score) => {
    if (score >= 80) return 'from-green-500 to-green-600';
    if (score >= 60) return 'from-yellow-500 to-yellow-600';
    if (score >= 40) return 'from-orange-500 to-orange-600';
    return 'from-red-500 to-red-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                AI Resume Analyzer
              </h1>
              <p className="text-gray-600 text-sm">Powered by Hugging Face 🤗</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Input Section */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Resume Upload */}
          <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center space-x-3 mb-4">
              <FileText className="w-6 h-6 text-indigo-600" />
              <h2 className="text-xl font-semibold text-gray-800">Upload Resume</h2>
            </div>
            
            <div className="space-y-4">
              <div 
                className="border-2 border-dashed border-indigo-300 rounded-lg p-8 text-center hover:border-indigo-500 transition-colors cursor-pointer bg-indigo-50"
                onClick={() => fileInputRef.current?.click()}
              >
                <Upload className="w-12 h-12 text-indigo-500 mx-auto mb-4" />
                <p className="text-gray-700 font-medium">Click to upload resume</p>
                <p className="text-gray-500 text-sm">PDF, DOCX, or TXT files</p>
                {uploadLoading && (
                  <div className="flex items-center justify-center mt-4">
                    <div className="animate-spin rounded-full h-6 w-6 border-2 border-indigo-500 border-t-transparent"></div>
                    <span className="ml-2 text-indigo-600">Processing...</span>
                  </div>
                )}
              </div>
              
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileUpload}
                className="hidden"
              />
              
              {resumeFile && (
                <div className="flex items-center space-x-2 text-green-600 bg-green-50 p-3 rounded-lg">
                  <CheckCircle className="w-5 h-5" />
                  <span className="text-sm font-medium">✅ {resumeFile.name}</span>
                </div>
              )}

              <textarea
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
                placeholder="Or paste resume text here..."
                className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              />
            </div>
          </div>

          {/* Job Description */}
          <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
            <div className="flex items-center space-x-3 mb-4">
              <Briefcase className="w-6 h-6 text-purple-600" />
              <h2 className="text-xl font-semibold text-gray-800">Job Description</h2>
            </div>
            
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            />
          </div>
        </div>

        {/* Analyze Button */}
        <div className="text-center mb-8">
          <button
            onClick={handleAnalyze}
            disabled={loading || !resumeText.trim() || !jobDescription.trim()}
            className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
          >
            {loading ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                <span>Analyzing...</span>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Zap className="w-5 h-5" />
                <span>Analyze Match</span>
              </div>
            )}
          </button>
        </div>

        {/* Results Section */}
        {analysis && (
          <div className="space-y-6">
            {/* Fit Score Card */}
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
              <div className="text-center">
                <div className={`text-6xl font-bold mb-2 ${getFitScoreColor(analysis.fit_score)}`}>
                  {analysis.fit_score}%
                </div>
                <div className={`text-lg font-semibold bg-gradient-to-r ${getFitScoreGradient(analysis.fit_score)} bg-clip-text text-transparent`}>
                  Match Score
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3 mt-4">
                  <div 
                    className={`h-3 rounded-full bg-gradient-to-r ${getFitScoreGradient(analysis.fit_score)}`}
                    style={{ width: `${analysis.fit_score}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Skills Analysis */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Matched Skills */}
              <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
                <div className="flex items-center space-x-3 mb-4">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                  <h3 className="text-xl font-semibold text-gray-800">Matched Skills</h3>
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm font-medium">
                    {analysis.matched_skills.length}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {analysis.matched_skills.map((skill, index) => (
                    <span key={index} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                      ✅ {skill}
                    </span>
                  ))}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
                <div className="flex items-center space-x-3 mb-4">
                  <AlertCircle className="w-6 h-6 text-orange-600" />
                  <h3 className="text-xl font-semibold text-gray-800">Missing Skills</h3>
                  <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded-full text-sm font-medium">
                    {analysis.missing_skills.length}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {analysis.missing_skills.map((skill, index) => (
                    <span key={index} className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-medium">
                      📚 {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* HR Summary */}
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
              <div className="flex items-center space-x-3 mb-4">
                <Star className="w-6 h-6 text-yellow-600" />
                <h3 className="text-xl font-semibold text-gray-800">HR Summary</h3>
              </div>
              <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg">
                {analysis.hr_summary}
              </p>
            </div>

            {/* Market Insights */}
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
              <div className="flex items-center space-x-3 mb-4">
                <TrendingUp className="w-6 h-6 text-blue-600" />
                <h3 className="text-xl font-semibold text-gray-800">Market Insights</h3>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(analysis.market_insights).map(([key, value], index) => (
                  <div key={index} className="bg-blue-50 p-4 rounded-lg">
                    <div className="text-blue-800 font-semibold capitalize mb-1">
                      {key.replace('_', ' ')}
                    </div>
                    <div className="text-blue-600">{value}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Improvement Suggestions */}
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
              <div className="flex items-center space-x-3 mb-4">
                <Target className="w-6 h-6 text-indigo-600" />
                <h3 className="text-xl font-semibold text-gray-800">Improvement Suggestions</h3>
              </div>
              <div className="space-y-3">
                {analysis.improvement_suggestions.map((suggestion, index) => (
                  <div key={index} className="flex items-start space-x-3 bg-indigo-50 p-4 rounded-lg">
                    <div className="text-indigo-600 font-bold">{index + 1}.</div>
                    <div className="text-gray-700">{suggestion}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeAnalyzer;
