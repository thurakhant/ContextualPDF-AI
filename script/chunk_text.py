import sys
import json
from pathlib import Path

# Add the src directory to the Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

print(f"Parent directory added to sys.path: {parent_dir}")

from src.preprocess.text_chunking import chunk_text

# Paths for input and output files
input_path = parent_dir / 'data' / 'processed' / 'cleaned_dart.txt'
output_path = parent_dir / 'data' / 'processed' / 'chunked_dart.json'

print(f"Input path: {input_path}")
print(f"Output path: {output_path}")

# Check if input file exists
if not input_path.exists():
    print(f"Error: Input file not found at {input_path}")
    sys.exit(1)

# Load cleaned text
cleaned_text = input_path.read_text(encoding='utf-8')

# Chunk the text
chunks = chunk_text(cleaned_text, max_chunk_size=1000)

# Save the chunks to a JSON file
output_path.write_text(json.dumps(chunks, indent=2), encoding='utf-8')

print(f"Text chunking completed. Output saved to: {output_path}")