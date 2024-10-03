import sys
from pathlib import Path

# Add the src directory to the Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.extract.pdf_extractor import extract_text_from_pdf

# Paths for input and output files
input_path = parent_dir / 'data' / 'raw' / 'dart.pdf'
output_path = parent_dir / 'data' / 'processed' / 'dart.txt'

# Extract text from the PDF
text = extract_text_from_pdf(str(input_path))

# Save the extracted text to a file
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(text)

print(f"Text extraction completed. Output saved to: {output_path}")