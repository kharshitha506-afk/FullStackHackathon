import pickle
import os

def load_model():
    """Load the trained ML model and vectorizer."""
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        print("Model files not found. Please train the model first.")
        return None, None

def predict_phishing(text, model, vectorizer):
    """
    Predict if text is phishing using ML model.
    Returns prediction and confidence score.
    """
    if model is None or vectorizer is None:
        return {
            'prediction': 'unknown',
            'confidence': 0.0,
            'error': 'Model not loaded'
        }
    
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    probabilities = model.predict_proba(text_vectorized)[0]
    
    confidence = probabilities[prediction]
    
    return {
        'prediction': 'phishing' if prediction == 1 else 'safe',
        'confidence': round(float(confidence) * 100, 2),
        'phishing_probability': round(float(probabilities[1]) * 100, 2),
        'safe_probability': round(float(probabilities[0]) * 100, 2)
    }

def calculate_final_verdict(rules, ml_result, triggers):
    """
    Calculate final phishing verdict based on all signals.
    Returns verdict with reasoning.
    """
    risk_score = 0
    
    high_severity_rules = sum(1 for rule in rules if rule['severity'] == 'high')
    medium_severity_rules = sum(1 for rule in rules if rule['severity'] == 'medium')
    
    risk_score += high_severity_rules * 30
    risk_score += medium_severity_rules * 15
    
    if ml_result.get('prediction') == 'phishing':
        risk_score += ml_result.get('confidence', 0) / 2
    
    risk_score += len(triggers) * 10
    
    risk_score = min(risk_score, 100)
    
    if risk_score >= 70:
        verdict = 'danger'
        label = 'HIGH RISK - Likely Phishing'
        recommendation = 'Do NOT click any links or provide information. Delete this message immediately.'
    elif risk_score >= 40:
        verdict = 'warning'
        label = 'SUSPICIOUS - Possible Phishing'
        recommendation = 'Exercise extreme caution. Verify sender through official channels before taking action.'
    else:
        verdict = 'safe'
        label = 'LOW RISK - Appears Safe'
        recommendation = 'Message appears legitimate, but always verify important requests independently.'
    
    return {
        'verdict': verdict,
        'label': label,
        'risk_score': round(risk_score, 1),
        'recommendation': recommendation
    }
