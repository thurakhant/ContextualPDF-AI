import sys
from pathlib import Path

# Add the src directory to the Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.preprocess.text_preprocessing import clean_text

# Paths for input and output files
input_path = parent_dir / 'data' / 'processed' / 'dart.txt'
output_path = parent_dir / 'data' / 'processed' / 'cleaned_dart.txt'

# Load extracted text
raw_text = input_path.read_text(encoding='utf-8')

# Clean the text
cleaned_text = clean_text(raw_text)

# Save the cleaned text to a new file
output_path.write_text(cleaned_text, encoding='utf-8')

print(f"Text cleaning completed. Output saved to: {output_path}")