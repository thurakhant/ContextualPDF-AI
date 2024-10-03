import re

def clean_text(text):
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Preserve chapter, title, and section numbers
    text = re.sub(r'(Chapter|Title|Section)\s+(\d+)', r'\n\1 \2\n', text)
    
    # Remove standalone page numbers
    text = re.sub(r'\b(?<!Chapter )(?<!Title )(?<!Section )\d+\b(?!\s*[A-Za-z])', '', text)
    
    # Remove headers or footers (customize as needed)
    text = re.sub(r'Page \d+', '', text)
    
    # Remove other common artifacts
    text = re.sub(r'^\s*-\s*\d+\s*-\s*$', '', text, flags=re.MULTILINE)  # Remove lines like "- 1 -"
    
    # Additional cleaning steps can be added here as needed
    
    return text.strip()

# ... (rest of the code remains the same)

if __name__ == '__main__':
    # Path to the extracted text file
    input_path = '../data/processed/social_security_act.txt'
    output_path = '../data/processed/cleaned_social_security_act.txt'
    
    # Read the extracted text
    with open(input_path, 'r', encoding='utf-8') as file:
        raw_text = file.read()
    
    # Clean the text
    cleaned_text = clean_text(raw_text)
    
    # Save the cleaned text to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
    
    print(f"Text cleaning completed. Cleaned output saved to: {output_path}")
