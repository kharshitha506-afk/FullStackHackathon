from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from rules import check_rules, detect_psychology_triggers, analyze_url
from utils import load_model, predict_phishing, calculate_final_verdict

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

model, vectorizer = load_model()

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/analyze_message', methods=['POST'])
def analyze_message():
    """Analyze text message for phishing indicators."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message']
        
        if not message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        rules_triggered = check_rules(message)
        
        psychology_triggers = detect_psychology_triggers(message)
        
        ml_prediction = predict_phishing(message, model, vectorizer)
        
        final_verdict = calculate_final_verdict(
            rules_triggered, 
            ml_prediction, 
            psychology_triggers
        )
        
        response = {
            'success': True,
            'analysis': {
                'rules': rules_triggered,
                'ml_prediction': ml_prediction,
                'psychology_triggers': psychology_triggers,
                'final_verdict': final_verdict
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/scan_url', methods=['POST'])
def scan_url():
    """Scan URL for phishing indicators."""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
        
        url = data['url']
        
        if not url.strip():
            return jsonify({'error': 'URL cannot be empty'}), 400
        
        url_checks = analyze_url(url)
        
        url_text = f"Visit this link: {url}"
        ml_prediction = predict_phishing(url_text, model, vectorizer)
        
        danger_count = sum(1 for check in url_checks if check['status'] == 'danger')
        warning_count = sum(1 for check in url_checks if check['status'] == 'warning')
        
        risk_score = (danger_count * 40) + (warning_count * 20)
        risk_score += ml_prediction.get('phishing_probability', 0) / 3
        risk_score = min(risk_score, 100)
        
        if risk_score >= 60:
            verdict = 'danger'
            label = 'DANGEROUS - Do Not Visit'
            recommendation = 'This URL shows strong phishing indicators. Do NOT click this link.'
        elif risk_score >= 30:
            verdict = 'warning'
            label = 'SUSPICIOUS - Proceed with Caution'
            recommendation = 'This URL has some suspicious characteristics. Verify before visiting.'
        else:
            verdict = 'safe'
            label = 'APPEARS SAFE'
            recommendation = 'URL appears legitimate, but always verify important links independently.'
        
        response = {
            'success': True,
            'analysis': {
                'url': url,
                'checks': url_checks,
                'ml_prediction': ml_prediction,
                'final_verdict': {
                    'verdict': verdict,
                    'label': label,
                    'risk_score': round(risk_score, 1),
                    'recommendation': recommendation
                }
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    if model is None or vectorizer is None:
        print("\n" + "="*60)
        print("WARNING: ML model not found!")
        print("Please run: python backend/train_model.py")
        print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
