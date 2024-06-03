import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, recall_score, average_precision_score
import numpy as np
import sys
from text_processing_2 import process_text
sys.path.append('.')


def calculate_precision_recall(relevantResult, retrieved, threshold=0.6):
    pred_binary = (retrieved >= threshold).astype(int)
    precision = precision_score(relevantResult, pred_binary, average='micro', zero_division=0)
    recall = recall_score(relevantResult, pred_binary, average='micro', zero_division=0)
    return precision, recall


def calculate_map_score(relevantResult, retrieved):
    return average_precision_score(relevantResult, retrieved, average='micro')


def loadData(file_path):
    try:
        data = pd.read_csv(file_path, delimiter='\t', header=None, names=['pid', 'text'])
    except pd.errors.ParserError as e:
        print(f"Error reading the dataset file: {e}")
        sys.exit(1)
    return data


def queries(queries_paths):
    queries = []
    for file_path in queries_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    query = json.loads(line.strip())
                    if 'query' in query:
                        queries.append(query)
                except json.JSONDecodeError:
                    print(f"Skipping invalid line in {file_path}: {line}")
    return queries


def processData(texts):
    processed_texts = []
    for text in texts:
        if isinstance(text, str):
            processed_text = process_text(text)
            processed_texts.append(processed_text)
        else:
            print("Skipping", text)
    return processed_texts


def createVector(texts):
    vector = TfidfVectorizer()
    try:
        matrix = vector.fit_transform(texts)
    except ValueError as e:
        print(f"Error")
        sys.exit(1)
    return matrix, vector


def searchQuery(query, tfidf_matrix, vectorizer, data):
    query_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(tfidf_matrix, query_vector).flatten()
    n = 10
    top_documents_index = cosine_similarities.argsort()[-n:][::-1]
    top_documents = data.iloc[top_documents_index]
    return top_documents, cosine_similarities[top_documents_index]


if __name__ == '__main__':
    
    dataset_path = r'C:\Users\hp\Desktop\IR_project_spyder\lotte\collection.tsv'
    dataSet = loadData(dataset_path)
    dataSet.dropna(subset=['text'], inplace=True)

    if 'text' not in dataSet.columns:
        sys.exit(1)

    processed_texts = processData(dataSet['text'])

    if not processed_texts:
        sys.exit(1)

    matrix, vector = createVector(processed_texts)
    
    queries_paths = [r'C:\Users\hp\Desktop\IR_project_spyder\lotte\qas.search.jsonl']
    queries = queries(queries_paths)

    precisions = []
    recalls = []
    map_avarage_precision = []

    for query in queries:
        if 'query' in query:
            resultQuery = process_text(query['query'])

            top_documents, cosine_similarities = searchQuery(resultQuery, matrix, vector, dataSet)

            relevance = np.zeros(len(dataSet))
            for pid in query.get('answer_pids', []):
                relevance[np.where(dataSet['pid'] == pid)[0]] = 1

            relevantResult = relevance[top_documents.index]
            retrieved = cosine_similarities
            if relevantResult.sum() == 0:
                continue

            precision, recall = calculate_precision_recall(relevantResult, retrieved)
            precisions.append(precision)
            recalls.append(recall)

            map_score = calculate_map_score(relevantResult, retrieved)
            map_avarage_precision.append(map_score)


    avg_precision = np.mean(precisions)
    avg_recall = np.mean(recalls)
    avg_map_score = np.mean(map_avarage_precision)

    print(f"Average Precision: {avg_precision}")
    print(f"Average Recall: {avg_recall}")
    print(f"Average MAP : {avg_map_score}")
    
