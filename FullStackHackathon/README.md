# PhishShield - Hybrid Phishing & Scam Detection System

A full-stack web application that uses machine learning, rule-based detection, and psychological analysis to identify phishing attempts in messages and URLs.

## 🎯 Project Overview

PhishShield is a comprehensive phishing detection system built for hackathon demonstration. It combines three powerful detection methods:

1. **Machine Learning**: TF-IDF vectorization + Logistic Regression classifier
2. **Rule-Based Engine**: Pattern matching for known phishing indicators
3. **Psychology Detection**: Identifies manipulation tactics (urgency, fear, authority, reward)

## 🏗️ Project Structure

```
.
├── backend/
│   ├── app.py                  # Flask API server
│   ├── rules.py                # Rule-based detection engine
│   ├── utils.py                # ML prediction utilities
│   ├── train_model.py          # Model training script
│   ├── phishing_dataset.csv    # Training dataset
│   ├── model.pkl               # Trained ML model
│   ├── vectorizer.pkl          # TF-IDF vectorizer
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── index.html              # Home page
│   ├── scan-message.html       # Message scanning interface
│   ├── scan-url.html           # URL scanning interface
│   ├── about.html              # About page
│   └── assets/
│       ├── style.css           # Styling
│       └── script.js           # Frontend logic
└── README.md                   # This file
```

## 🚀 Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)
- Bootstrap 5

### Backend
- Python 3.11
- Flask (Web Framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- scikit-learn (Machine Learning)
- pandas (Data Processing)

## 📦 Setup & Installation

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install Flask Flask-CORS scikit-learn pandas
   ```

2. **Train the ML Model**
   ```bash
   python backend/train_model.py
   ```
   
   This will:
   - Load the phishing dataset
   - Train a Logistic Regression model
   - Save model.pkl and vectorizer.pkl

3. **Start the Flask Application**
   ```bash
   python backend/app.py
   ```
   
   The Flask server will start on `http://0.0.0.0:5000` and automatically serve both:
   - The frontend UI (HTML/CSS/JS from the `/frontend` folder)
   - The backend API endpoints (`/analyze_message`, `/scan_url`)

4. **Access the Application**
   - Navigate to `http://localhost:5000` in your browser
   - Or use the Replit webview to access the application
   - The frontend is served directly by Flask (no separate static server needed)

## 🔌 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Analyze Message
**POST** `/analyze_message`

Analyzes text message for phishing indicators.

**Request Body:**
```json
{
  "message": "Your account has been suspended. Click here immediately!"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "rules": [...],
    "ml_prediction": {
      "prediction": "phishing",
      "confidence": 85.5,
      "phishing_probability": 85.5,
      "safe_probability": 14.5
    },
    "psychology_triggers": [...],
    "final_verdict": {
      "verdict": "danger",
      "label": "HIGH RISK - Likely Phishing",
      "risk_score": 87.5,
      "recommendation": "Do NOT click any links..."
    }
  }
}
```

#### 2. Scan URL
**POST** `/scan_url`

Scans URL for phishing indicators.

**Request Body:**
```json
{
  "url": "http://suspicious-site.tk/verify-account"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "url": "http://suspicious-site.tk/verify-account",
    "checks": [...],
    "ml_prediction": {...},
    "final_verdict": {...}
  }
}
```

## 🧪 Testing the Application

### Test with Sample Messages

**Phishing Example:**
```
URGENT: Your account has been suspended. Verify immediately or lose access.
```

**Safe Example:**
```
Meeting scheduled for tomorrow at 2 PM in conference room B.
```

### Test with Sample URLs

**Suspicious URL:**
```
http://verify-account.tk/login
```

**Safe URL:**
```
https://www.google.com
```

## 🎨 Features

### Message Scanning
- Text analysis for phishing patterns
- ML-based classification
- Rule-based detection
- Psychology trigger identification
- Risk scoring (0-100)
- Color-coded verdicts

### URL Scanning
- Protocol validation (HTTP/HTTPS)
- Domain analysis
- TLD checking
- Pattern matching
- ML scoring
- Comprehensive safety checks

### Detection Methods

1. **Rule-Based Detection**
   - Urgency keywords
   - Money/prize mentions
   - Threatening language
   - Brand impersonation
   - Suspicious URLs
   - Multiple link detection

2. **Machine Learning**
   - TF-IDF feature extraction
   - Logistic Regression classifier
   - Confidence scoring
   - Probability distribution

3. **Psychology Triggers**
   - Urgency (time pressure)
   - Fear (threats, consequences)
   - Authority (impersonation)
   - Reward (too-good-to-be-true offers)

## 📊 Model Performance

- **Accuracy**: ~73%
- **Dataset Size**: 51 samples (25 phishing, 26 safe)
- **Algorithm**: Logistic Regression
- **Features**: TF-IDF (1000 max features, 1-2 ngrams)

## 🔒 Security Notes

- This is a demonstration project for educational purposes
- The ML model is trained on a small dataset and should not be used for production security decisions
- Always verify suspicious content through official channels
- Never share sensitive information based solely on automated analysis

## 🚧 Limitations

- Small training dataset (limited to 51 samples)
- No real-time URL reputation checking
- No email header analysis
- No link following or content inspection
- Basic pattern matching only

## 🔮 Future Enhancements

- Larger, more diverse training dataset
- Deep learning models (BERT, transformers)
- URL reputation API integration
- Email header analysis
- Browser extension
- User feedback loop
- Detection history dashboard
- Multi-language support

## 👥 Team

Built as a hackathon project demonstrating full-stack development and machine learning integration.

## 📄 License

This project is for educational purposes only.

## 🙏 Acknowledgments

- Built with Flask and scikit-learn
- Bootstrap for UI components
- Replit for hosting environment

---

**Stay Safe Online! 🛡️**
