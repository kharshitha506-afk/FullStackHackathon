# PhishShield Project

## Overview
PhishShield is a full-stack hackathon project that detects phishing attempts and scams using a hybrid approach combining machine learning, rule-based detection, and psychological analysis.

**Purpose**: Demonstrate full-stack development skills with ML integration for cybersecurity  
**Status**: ✅ Complete and functional  
**Built**: November 2024

## Architecture

### Backend (Python Flask)
- **Location**: `/backend`
- **Port**: 5000
- **Main Files**:
  - `app.py` - Flask API server with CORS enabled
  - `rules.py` - Rule-based phishing detection engine
  - `utils.py` - ML prediction utilities
  - `train_model.py` - Model training script
  - `phishing_dataset.csv` - Training data (51 samples)
  - `model.pkl` - Trained Logistic Regression model
  - `vectorizer.pkl` - TF-IDF vectorizer

### Frontend (HTML/CSS/JS)
- **Location**: `/frontend`
- **Framework**: Vanilla JavaScript + Bootstrap 5
- **Pages**:
  - `index.html` - Home page with project intro
  - `scan-message.html` - Message analysis interface
  - `scan-url.html` - URL scanning interface
  - `about.html` - Project information
  - `assets/style.css` - Custom styling
  - `assets/script.js` - API integration logic

## Features Implemented

### 1. Message Analysis
- ✅ Text input with textarea
- ✅ Rule-based detection (urgency, money, threats, impersonation)
- ✅ ML prediction with confidence scores
- ✅ Psychology trigger identification (urgency, fear, authority, reward)
- ✅ Final verdict with risk score (0-100)
- ✅ Color-coded alerts (danger/warning/safe)

### 2. URL Scanning
- ✅ URL input field
- ✅ Multiple safety checks (HTTPS, TLD, format, subdomains)
- ✅ ML-based phishing prediction
- ✅ Domain analysis and pattern matching
- ✅ Comprehensive risk assessment

### 3. Machine Learning
- ✅ TF-IDF vectorization (1000 features, 1-2 ngrams)
- ✅ Logistic Regression classifier
- ✅ 73% accuracy on test set
- ✅ Confidence scoring with probabilities

## API Endpoints

### POST /analyze_message
Analyzes text message for phishing indicators.

**Input**: `{ "message": "text to analyze" }`  
**Output**: Rules, ML prediction, psychology triggers, final verdict

### POST /scan_url
Scans URL for phishing indicators.

**Input**: `{ "url": "http://example.com" }`  
**Output**: Safety checks, ML prediction, final verdict

## Recent Changes

**November 21, 2024**
- ✅ Created complete backend with Flask API
- ✅ Implemented rule-based detection engine
- ✅ Built ML model training pipeline
- ✅ Created frontend with 4 responsive pages
- ✅ Integrated frontend-backend communication
- ✅ Trained phishing detection model (73% accuracy)
- ✅ Configured Flask workflow on port 5000
- ✅ Added comprehensive documentation

## Tech Stack

**Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5  
**Backend**: Python 3.11, Flask, Flask-CORS  
**ML**: scikit-learn (TF-IDF + Logistic Regression), pandas  
**Deployment**: Replit with workflow automation

## Running the Project

### Start Backend
The Flask server runs automatically via the configured workflow:
```bash
python backend/app.py
```
Server runs on `http://0.0.0.0:5000`

### Access Frontend
Open the Replit webview or navigate to the deployed URL to access the application.

### Training the Model
If model files are missing:
```bash
python backend/train_model.py
```

## Dependencies Installed
- Flask 3.1.2
- Flask-CORS 6.0.1
- scikit-learn 1.7.2
- pandas 2.3.3
- numpy 2.3.5

## Project Structure
```
PhishShield/
├── backend/          # Flask API and ML
├── frontend/         # HTML/CSS/JS interface
├── README.md         # Full documentation
├── .gitignore        # Python gitignore
└── replit.md         # This file
```

## Known Limitations
- Small training dataset (51 samples)
- No real-time URL reputation checking
- No email header analysis
- Development server (not production-ready)

## Future Enhancements
- Larger training dataset
- Deep learning models (BERT)
- URL reputation API integration
- Browser extension
- User feedback system
- Detection history dashboard
