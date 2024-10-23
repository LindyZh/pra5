from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import json

application = Flask(__name__)

@application.route("/")
def index():
    return "Your Flask App Works! V1.0"

def load_model():
    load_model, vectorizer = None, None
    with open('basic_classifier.pkl', 'rb') as f:
        load_model = pickle.load(f)
    with open('count_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return load_model, vectorizer

model, vectorizer = load_model()

@application.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data['text']
    prediction = model.predict(vectorizer.transform([text]))[0]
    return jsonify({"prediction": prediction})


if __name__ == "__main__":
    application.run()