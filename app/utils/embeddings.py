# app/services/embedding_manager.py

from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the pre-trained model (768-dimensional to match Pinecone index)
model = SentenceTransformer('all-mpnet-base-v2')  # This model returns 768-dimensional vectors

def embed_text(text: str) -> np.ndarray:
    """
    Convert text into a dense vector using Sentence-BERT.
    """
    embedding = model.encode(text)
    return embedding

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calculate the cosine similarity between two vectors.
    """
    cosine_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return float(cosine_sim)
