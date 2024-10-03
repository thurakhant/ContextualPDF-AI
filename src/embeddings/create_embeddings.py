import json
import openai
from tqdm import tqdm
import time
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_embedding(text):
    try:
        response = openai.embeddings.create(
            input=[text],
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error creating embedding for text: {text[:50]}...: {e}")
        return None

def create_embeddings_batch(chunks):
    embeddings = []
    for chunk in tqdm(chunks, desc="Processing batches"):
        try:
            # Truncate the chunk if it's too long
            truncated_chunk = chunk[:8000]  # Adjust this value as needed
            response = openai.embeddings.create(
                model="text-embedding-ada-002",
                input=truncated_chunk
            )
            embeddings.append(response.data[0].embedding)
        except openai.BadRequestError as e:
            print(f"Error creating embedding: {e}")
            continue  # Skip this chunk and continue with the next
        except openai.RateLimitError:
            time.sleep(60)  # Wait for 60 seconds before retrying
    return embeddings

if __name__ == '__main__':
    # Get the project root directory
    project_root = Path(__file__).resolve().parent.parent.parent

    # Paths to input and output files
    input_path = project_root / 'data' / 'processed' / 'chunked_social_security_act.json'
    output_path = project_root / 'data' / 'processed' / 'social_security_act_with_embeddings.json'
    
    # Load chunked text
    chunks = json.loads(input_path.read_text(encoding='utf-8'))
    
    print(f"Loaded {len(chunks)} chunks from {input_path}")

    # Debugging lines to inspect the data
    print(f"Type of chunks: {type(chunks)}")
    print(f"Type of first chunk: {type(chunks[0])}")
    print(f"First chunk content: {chunks[0][:100]}") 
    
    # Create embeddings for chunks in batches
    embeddings = create_embeddings_batch(chunks)

    # Verify the number of embeddings matches the number of chunks
    if len(embeddings) != len(chunks):
        print(f"Error: Number of embeddings ({len(embeddings)}) does not match number of chunks ({len(chunks)})")
    else:
        print(f"Created {len(embeddings)} embeddings")
        
        # Combine chunks with their embeddings
        chunks_with_embeddings = [
            {'text': chunk, 'embedding': embedding}
            for chunk, embedding in zip(chunks, embeddings)
        ]
        
        # Save the chunks with embeddings to a JSON file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(chunks_with_embeddings, indent=2, ensure_ascii=False), encoding='utf-8')
        
        print(f"Embedding creation completed. Output saved to: {output_path}")