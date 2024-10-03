import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).resolve().parent.parent

# Add the src/chatbot directory to the Python path
sys.path.append(str(project_root / 'src' / 'chatbot'))

from chatbot import run_chatbot

if __name__ == '__main__':
    # Path to the file containing chunks with embeddings
    embedding_file_path = project_root / 'data' / 'processed' / 'dart_with_embeddings.json'
    
    # Check if the embedding file exists
    if not embedding_file_path.exists():
        print(f"Error: Embedding file not found at {embedding_file_path}")
        print("Please make sure you have run the embedding creation script first.")
        sys.exit(1)

    print(f"Using embedding file: {embedding_file_path}")
    
    # Run the chatbot
    run_chatbot(str(embedding_file_path))

print("Chatbot session ended.")