import fitz
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    text = ''
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                page_text = page.get_text()
                if page_text:
                    text += page_text + '\n'  # Add a newline for better readability
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return None
    return text

if __name__ == '__main__':
    # Path to the PDF file
    pdf_path = '../data/raw/dart.pdf'
    
    # Extract text
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if extracted_text is not None:
        # Save the extracted text to a file in data/processed/
        output_path = '../data/processed/Social_Security_Act.txt'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(extracted_text)
        
        print(f"Text extraction completed. Output saved to: {output_path}")
    else:
        print("Text extraction failed. No output file was created.")