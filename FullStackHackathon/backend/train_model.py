import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

def train_phishing_model():
    """Train a phishing detection model using TF-IDF and Logistic Regression."""
    
    print("Loading dataset...")
    script_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(script_dir, 'phishing_dataset.csv')
    df = pd.read_csv(dataset_path)
    
    print(f"Dataset loaded: {len(df)} samples")
    print(f"Phishing: {sum(df['label'] == 1)}, Safe: {sum(df['label'] == 0)}")
    
    X = df['text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("\nVectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=1
    )
    
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)
    
    print("Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        C=1.0
    )
    
    model.fit(X_train_vectorized, y_train)
    
    y_pred = model.predict(X_test_vectorized)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Phishing']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    model_path = os.path.join(script_dir, 'model.pkl')
    vectorizer_path = os.path.join(script_dir, 'vectorizer.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print(f"\nModel saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")
    
    print("\n" + "="*50)
    print("Training completed successfully!")
    print("="*50)

if __name__ == '__main__':
    train_phishing_model()
