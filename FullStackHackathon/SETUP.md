# PhishShield Setup Guide

This guide will help you set up and run PhishShield on Replit or your local machine.

## 🚀 Quick Start (Replit)

1. **The project is already set up and running!**
   - Click the "Run" button or refresh the webview
   - The Flask backend starts automatically on port 5000
   - Access the frontend through the Replit webview

2. **If the model is missing, train it:**
   ```bash
   python backend/train_model.py
   ```

3. **Access the application:**
   - Use the Replit webview to interact with PhishShield
   - Navigate between pages using the top navigation bar

## 🔧 Local Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd PhishShield
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install Flask Flask-CORS scikit-learn pandas
   ```

3. **Train the ML model**
   ```bash
   python backend/train_model.py
   ```
   
   Expected output:
   ```
   Loading dataset...
   Dataset loaded: 51 samples
   Training Logistic Regression model...
   Model Accuracy: ~73%
   Model saved to: backend/model.pkl
   ```

4. **Start the Flask backend**
   ```bash
   python backend/app.py
   ```
   
   The server will start on `http://0.0.0.0:5000`

5. **Access the frontend**
   - Open `frontend/index.html` in your web browser
   - Or serve it with a local server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
   - Navigate to `http://localhost:8000`

## 📋 Verification Steps

### 1. Check Backend is Running
Visit `http://localhost:5000` in your browser. You should see:
```json
{
  "message": "PhishShield API is running",
  "version": "1.0",
  "endpoints": [
    "/analyze_message (POST)",
    "/scan_url (POST)"
  ]
}
```

### 2. Test Message Analysis
```bash
curl -X POST http://localhost:5000/analyze_message \
  -H "Content-Type: application/json" \
  -d '{"message": "URGENT: Your account has been suspended!"}'
```

### 3. Test URL Scanning
```bash
curl -X POST http://localhost:5000/scan_url \
  -H "Content-Type: application/json" \
  -d '{"url": "http://suspicious-site.tk"}'
```

## 🎯 Usage Guide

### Scanning Messages

1. Navigate to "Scan Message" page
2. Paste any suspicious message in the text area
3. Click "Analyze Message"
4. Review the results:
   - **Verdict badge** (High Risk / Suspicious / Low Risk)
   - **ML Prediction** with confidence score
   - **Rule-based detections** showing triggered patterns
   - **Psychology triggers** identifying manipulation tactics

### Scanning URLs

1. Navigate to "Scan URL" page
2. Enter a URL (include http:// or https://)
3. Click "Scan URL"
4. Review the results:
   - **Safety checks** for HTTPS, domain, format
   - **ML score** for phishing probability
   - **Final verdict** with recommendations

## 🔍 Testing Examples

### Phishing Messages to Test
```
Example 1: Urgency + Threat
"URGENT: Your account has been suspended. Verify immediately or lose access."

Example 2: Prize/Reward
"Congratulations! You've won $1000. Click here to claim your prize now!"

Example 3: Authority + Fear
"IRS Notice: You owe $5000 in back taxes. Pay immediately to avoid arrest."
```

### Safe Messages to Test
```
Example 1: Work Communication
"Meeting scheduled for tomorrow at 2 PM in conference room B."

Example 2: Legitimate Order
"Your order has shipped and will arrive on Thursday. Thank you for shopping!"
```

### URLs to Test
```
Suspicious URLs:
- http://verify-account.tk/login
- http://paypal-security-check.ml/update
- http://www.bank-account-verify.xyz

Safe URLs:
- https://www.google.com
- https://github.com
- https://www.wikipedia.org
```

## 🛠️ Troubleshooting

### Issue: "Model files not found"
**Solution**: Run the training script
```bash
python backend/train_model.py
```

### Issue: "Connection refused" or "CORS error"
**Solution**: 
1. Ensure Flask backend is running
2. Check that Flask-CORS is installed
3. Verify the API_BASE_URL in `frontend/assets/script.js`

### Issue: Frontend not calling backend
**Solution**: 
- Open browser console (F12) to check for errors
- Verify the backend URL in `script.js` matches your Flask server
- Check that CORS is enabled in `app.py`

### Issue: Low model accuracy
**Solution**: 
- This is expected with the small dataset (51 samples)
- For better accuracy, expand `phishing_dataset.csv` with more examples
- Retrain the model with more data

## 📦 Dependencies Reference

### Python Packages
- **Flask** (3.1.2): Web framework
- **Flask-CORS** (6.0.1): Cross-origin resource sharing
- **scikit-learn** (1.7.2): Machine learning
- **pandas** (2.3.3): Data manipulation
- **numpy** (2.3.5): Numerical operations

### Frontend Libraries (CDN)
- **Bootstrap** (5.3.2): UI framework
- Loaded via CDN, no installation needed

## 🚀 Deployment

### Deploy to Replit
1. The project is already configured for Replit
2. Use the "Deploy" button in Replit
3. Your app will be publicly accessible

### Deploy Elsewhere
For production deployment:
1. Use a production WSGI server (gunicorn, uWSGI)
2. Set up proper environment variables
3. Use a reverse proxy (nginx)
4. Enable HTTPS
5. Consider rate limiting and authentication

Example with gunicorn:
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --chdir backend app:app
```

## 📚 Additional Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **scikit-learn**: https://scikit-learn.org/
- **Bootstrap**: https://getbootstrap.com/

## 💡 Tips

1. **Expanding the Dataset**: Add more examples to `phishing_dataset.csv` and retrain
2. **Customizing Rules**: Modify `backend/rules.py` to add new detection patterns
3. **Adjusting Risk Scores**: Edit `backend/utils.py` to change how risk is calculated
4. **Styling**: Customize `frontend/assets/style.css` for different looks

---

**Need Help?** Check the main README.md for more detailed information.
