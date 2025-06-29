import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample Documents
documents = [
    "The sky is blue and beautiful.",
    "Love this blue and beautiful sky!",
    "The quick brown fox jumps over the lazy dog.",
    "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
    "I love green eggs, ham, sausages and bacon!",
    "The brown fox is quick and the blue dog is lazy!",
    "The sky is very blue and the sky is very beautiful today",
    "The dog is lazy but the brown fox is quick!"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)
vector_database = X.toarray() # Store the document vector into arrays

def cosine_similarity_search(query, database, vectorizer, top_n=5): 
    """
    The function to perform similarity matching on query (a text).
    Returns: matches, and similarity scores.
    """
    
    query_vec = vectorizer.transform([query]).toarray()
    similarities = cosine_similarity(query_vec, database)[0]
    top_indices = np.argsort(-similarities)[:top_n] # Top n indices
    return [(idx, similarities[idx]) for idx in top_indices]

while True: 
    query = input("Enter a search query/text/word (or 'exit' to stop): ")
    if query.lower() == 'exit': 
        break 
    top_n = int(input("How many top matches do you want to see? "))
    search_results = cosine_similarity_search(
        query,
        vector_database, 
        vectorizer, 
        top_n
    )
    print("Top Matches Documents:")
    for idx, score in search_results: 
        print(f"- {documents[idx]} (Score: {score:.4f}) {score}")
        
    print("\n")
    
    