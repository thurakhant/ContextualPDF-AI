import json
from search.semantic_search import semantic_search

class KnowledgeBase:
    def __init__(self, embedding_file_path):
        self.embedding_file_path = embedding_file_path
        self.chunks_with_embeddings = self.load_embeddings()

    def load_embeddings(self):
        try:
            with open(self.embedding_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File {self.embedding_file_path} not found.")
            return []

    def search(self, query, top_n=3):
        if not self.chunks_with_embeddings:
            print("Error: No embeddings loaded.")
            return []
        
        # Use semantic search to find the most relevant chunks
        return semantic_search(query, self.chunks_with_embeddings, top_n=top_n)

# Example usage
if __name__ == '__main__':
    # Path to the file containing chunks with embeddings
    embedding_file_path = '../../data/processed/chunked_programming_book_with_embeddings.json'
    
    # Initialize the knowledge base
    knowledge_base = KnowledgeBase(embedding_file_path)
    
    # Example query
    query = "How do I define a class in Dart?"
    
    # Perform a search in the knowledge base
    top_chunks = knowledge_base.search(query, top_n=3)
    
    # Print the results
    print("Top relevant chunks for the query:")
    for idx, chunk in enumerate(top_chunks):
        print(f"{idx + 1}: {chunk}\n")
