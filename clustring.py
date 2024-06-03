import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import umap.umap_ as umap

# Load the saved vectorizer and TF-IDF matrix
vectorizer_file_path = r'C:\Users\hp\Desktop\IR_project\lotte\vectorizer.pkl'
tfidf_matrix_file_path = r'C:\Users\hp\Desktop\IR_project\lotte\tfidf_matrix.pkl'

with open(vectorizer_file_path, 'rb') as file:
    vectorizer = pickle.load(file)

with open(tfidf_matrix_file_path, 'rb') as file:
    tfidf_matrix = pickle.load(file)

# Load your dataset
dataset_path = r'C:\Users\hp\Desktop\IR_project_spyder\lotte\collection.tsv'
dataSet = pd.read_csv(dataset_path, delimiter='\t', header=None, names=['pid', 'text'])
dataSet.dropna(subset=['text'], inplace=True)

# Function to sample data
def sample_data(dataSet, sample_size):
    sampled_data = dataSet.sample(n=sample_size, random_state=42)
    return sampled_data

# Define sample size
sample_size = 1000  # Number of samples to use

# Sample data
sampled_data = sample_data(dataSet, sample_size)

# Filter the TF-IDF matrix to include only the sampled documents
sampled_indices = sampled_data.index
sampled_tfidf_matrix = tfidf_matrix[sampled_indices]

# Perform UMAP
reducer = umap.UMAP(n_components=2, random_state=42)
reduced_matrix_umap = reducer.fit_transform(sampled_tfidf_matrix)

# Perform K-Means clustering
num_clusters = 7
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(reduced_matrix_umap)  # Call fit method

# Plot the results
plt.figure(figsize=(12, 8))
plt.scatter(reduced_matrix_umap[:, 0], reduced_matrix_umap[:, 1], c=kmeans.labels_, cmap='viridis')
plt.colorbar()
plt.title('UMAP reduction and K-Means clustering')
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.show()
