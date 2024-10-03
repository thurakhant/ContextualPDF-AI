import os
import json
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def load_embeddings(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def semantic_search(query, chunks_with_embeddings, top_n=3):
    # Check for an exact match in the chunk text
    exact_matches = [chunk['text'] for chunk in chunks_with_embeddings if query.lower() in chunk['text'].lower()]
    if exact_matches:
        return exact_matches[:top_n]

    # Fallback to the existing semantic search using embeddings if no exact match found
    query_embedding = create_embedding(query)
    query_embedding_np = np.array(query_embedding).reshape(1, -1)
    chunk_embeddings_np = np.array([chunk['embedding'] for chunk in chunks_with_embeddings])
    
    # Compute cosine similarity
    similarities = cosine_similarity(query_embedding_np, chunk_embeddings_np)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    
    return [chunks_with_embeddings[i]['text'] for i in top_indices]

if __name__ == '__main__':
    # Path to the file containing chunks with embeddings
    input_path = 'data/processed/chunked_programming_book_with_embeddings.json'
    
    # Load the chunks with embeddings
    chunks_with_embeddings = load_embeddings(input_path)
    
    # Example query for testing
    query = "How do I define a class in Dart?"
    
    # Perform semantic search
    top_chunks = semantic_search(query, chunks_with_embeddings, top_n=3)
    
    # Print the results
    print("Top relevant chunks for the query:")
    for idx, chunk in enumerate(top_chunks):
        print(f"{idx + 1}: {chunk}\n")
