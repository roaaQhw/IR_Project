from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys
import pickle
from text_processing_2 import process_text
sys.path.append('.')

app = Flask(__name__)

def loadData(file_path):
    try:
        data = pd.read_csv(file_path, delimiter='\t', header=None, names=['pid', 'text'])
    except pd.errors.ParserError as e:
        print(f"Error reading the dataset file: {e}")
        sys.exit(1)
    return data

def processData(texts):
    processed_texts = []
    for text in texts:
        if isinstance(text, str):
            processed_text = process_text(text)
            processed_texts.append(processed_text)
        else:
            print("Skipping", text)
    return processed_texts

def searchQuery(query, tfidf_matrix, vectorizer, data):
    query_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(tfidf_matrix, query_vector).flatten()
    n = 10
    top_documents_index = cosine_similarities.argsort()[-n:][::-1]
    top_documents = data.iloc[top_documents_index]
    return top_documents['text'].tolist(), cosine_similarities[top_documents_index]

@app.route('/search_lifestyle', methods=['POST'])
def handle_query():
    try:
        request_data = request.get_json()
        query = request_data['query']
        result_query = process_text(query)
        top_documents_texts, cosine_similarities = searchQuery(result_query, matrix, vector, dataSet)
        return jsonify({"top_documents": top_documents_texts})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':

    # Load dataset and models
    dataset_path = r'C:\Users\hp\Desktop\IR_project_spyder\lotte\collection.tsv'
    dataSet = loadData(dataset_path)
    dataSet.dropna(subset=['text'], inplace=True)

    if 'text' not in dataSet.columns:
        sys.exit(1)

    # Load the saved TF-IDF matrix and vectorizer
    with open(r'C:\Users\hp\Desktop\IR_project\lotte\tfidf_matrix.pkl', 'rb') as file:
        matrix = pickle.load(file)

    with open(r'C:\Users\hp\Desktop\IR_project\lotte\vectorizer.pkl', 'rb') as file:
        vector = pickle.load(file)

    # Run Flask app
    app.run(port=5003)
