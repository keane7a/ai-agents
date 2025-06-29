from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

def get_embedding(text, model="text-embedding-004"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

# Sample documents
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

# Generate embeddings for each document 
embeddings = [get_embedding(doc) for doc in documents]
ids = [f"id{i}" for i in range(len(documents))]

# Init Chroma DB client
chorma_client = chromadb.Client()
collection = chorma_client.create_collection(name="documents")

# Add document to embeddings to the collection
collection.add(
    embeddings=embeddings, 
    documents=documents, 
    ids=ids
)

def query_chromadb(query, top_n=2): 
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n,
    )
    
    return [
        (id, score, text) for id, score, text in 
        zip(results["ids"][0], 
            results["distances"][0], 
            results["documents"][0])
    ]
    

while True: 
    query = input("Enter a search query (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    top_n = int(input("How many top matches do you want to see? "))
    search_results = query_chromadb(query, top_n)
    
    ###
    # Note: uses cosine distance and ranges between 0 and 2 where 0 for most similar and 2 for opposite meaning.
    ###
    print("Top Matched Documents:")
    for id, score, text in search_results:
        print(f"ID:{id} TEXT: {text} DISTANCE: {round(score, 2)}")

    print("\n")