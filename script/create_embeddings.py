import sys
import json
from pathlib import Path

# Add the src directory to the Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.embeddings.create_embeddings import create_embedding, create_embeddings_batch

# Paths for input and output files
input_path = parent_dir / 'data' / 'processed' / 'chunked_dart.json'
output_path = parent_dir / 'data' / 'processed' / 'dart_with_embeddings.json'

# Load chunked text
chunks = json.loads(input_path.read_text(encoding='utf-8'))

# Create embeddings for each chunk in batches
embeddings = create_embeddings_batch(chunks)

# Combine chunks with their embeddings
chunks_with_embeddings = [
    {'text': chunk, 'embedding': embedding}
    for chunk, embedding in zip(chunks, embeddings)
]

# Save the chunks with embeddings to a JSON file
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(chunks_with_embeddings, indent=2, ensure_ascii=False), encoding='utf-8')

print(f"Embedding creation completed. Output saved to: {output_path}")
