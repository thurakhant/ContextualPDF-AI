import json
from pathlib import Path
import re

def chunk_text(text, max_chunk_size=1000):
    # Split the text into chapters, titles, and sections
    chapter_pattern = r'(Chapter \d+)'
    title_pattern = r'(Title \d+)'
    section_pattern = r'(Section \d+)'
    
    # First, split by chapters
    chapters = re.split(chapter_pattern, text)
    chunks = []
    
    for i in range(0, len(chapters), 2):
        chapter_header = chapters[i] if i > 0 else ""
        chapter_content = chapters[i+1] if i+1 < len(chapters) else ""
        
        # Split chapter content by titles
        titles = re.split(title_pattern, chapter_content)
        for j in range(0, len(titles), 2):
            title_header = titles[j] if j > 0 else ""
            title_content = titles[j+1] if j+1 < len(titles) else ""
            
            # Split title content by sections
            sections = re.split(section_pattern, title_content)
            current_chunk = f"{chapter_header} {title_header}"
            
            for k in range(0, len(sections), 2):
                section_header = sections[k] if k > 0 else ""
                section_content = sections[k+1] if k+1 < len(sections) else ""
                
                potential_chunk = f"{current_chunk} {section_header} {section_content}".strip()
                
                if len(potential_chunk) > max_chunk_size and current_chunk != f"{chapter_header} {title_header}":
                    chunks.append(current_chunk.strip())
                    current_chunk = f"{chapter_header} {title_header} {section_header} {section_content}"
                else:
                    current_chunk = potential_chunk
            
            if current_chunk:
                chunks.append(current_chunk.strip())
    
    return chunks



if __name__ == '__main__':
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent.parent

    # Paths to input and output files
    input_path = project_root / 'data' / 'processed' / 'cleaned_programming_book.txt'
    output_path = project_root / 'data' / 'processed' / 'chunked_programming_book.json'
    
    # Read the cleaned text
    cleaned_text = input_path.read_text(encoding='utf-8')
    
    # Chunk the text
    chunks = chunk_text(cleaned_text, max_chunk_size=500)
    
    # Save the chunks to a JSON file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"Text chunking completed. Output saved to: {output_path}")