# LongChat-PDF: AI-Powered Conversational Interface for PDF Documents

## Purpose

LongChat-PDF is an advanced conversational AI system designed to interact with users based on the content of any given PDF document. It leverages natural language processing and semantic search technologies to provide accurate, context-aware responses while maintaining long-term conversation coherence.

## Key Features

- PDF text extraction and preprocessing
- Semantic chunking of document content
- Advanced embedding generation for text segments
- Efficient semantic search functionality
- Long-term context management in conversations
- Integration with OpenAI's GPT model for natural language generation

## Detailed Approach

1. **Text Extraction and Cleaning**:
   - Extract raw text from the input PDF using the `fitz` library.
   - Clean and normalize the extracted text, removing irrelevant information and standardizing format.

2. **Text Chunking**:
   - Split the cleaned text into semantically meaningful chunks.
   - Optimize chunk size for balance between context preservation and search efficiency.

3. **Embedding Creation**:
   - Generate vector representations (embeddings) for each text chunk using OpenAI's text-embedding-ada-002 model.
   - Store embeddings alongside text chunks for efficient retrieval.

4. **Knowledge Base Construction**:
   - Create a searchable knowledge base from the embedded text chunks.
   - Implement efficient indexing for fast query processing.

5. **Semantic Search**:
   - Convert user queries into embeddings.
   - Use cosine similarity to identify the most relevant text chunks.
   - Retrieve top-k most similar chunks for each query.

6. **Conversational Interface**:
   - Maintain conversation history for context-aware responses.
   - Combine relevant text chunks with conversation history.
   - Use OpenAI's GPT model to generate coherent and informative responses.

7. **Long-Term Context Management**:
   - Implement mechanisms to maintain context over extended conversations.
   - Summarize and store key points from the ongoing dialogue.
   - Periodically refresh context to keep responses relevant and accurate.

## System Components

1. **PDF Extractor** (`src/extract/pdf_extractor.py`):
   Handles the extraction of text content from PDF files.

2. **Text Preprocessor** (`src/preprocess/text_preprocessing.py`):
   Cleans and normalizes the extracted text.

3. **Text Chunker** (`src/preprocess/text_chunking.py`):
   Splits preprocessed text into manageable, semantic chunks.

4. **Embedding Generator** (`src/embeddings/create_embeddings.py`):
   Creates vector representations of text chunks using OpenAI's API.

5. **Semantic Search Engine** (`src/search/semantic_search.py`):
   Implements similarity-based search functionality for finding relevant text chunks.

6. **Knowledge Base** (`src/chatbot/knowledge_base.py`):
   Manages the storage, indexing, and retrieval of embedded text chunks. Features include:
   - Efficient loading of preprocessed and embedded chunks.
   - Fast semantic similarity search for query processing.
   - Caching mechanisms for improved response times.
   - Extensible design for future updates and improvements.

7. **Chatbot Core** (`src/chatbot/chatbot.py`):
   Orchestrates the conversation flow, integrating all components to generate responses.

## Setup and Usage

1. **Environment Setup**:
   ```
   git clone https://github.com/yourusername/LongChat-PDF.git
   cd LongChat-PDF
   pip install -r requirements.txt
   ```

2. **Configuration**:
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

3. **PDF Processing**:
   ```
   python script/extract_text.py
   python script/clean_text.py
   python script/chunk_text.py
   python script/create_embeddings.py
   ```

4. **Launch Chatbot**:
   ```
   python script/run_chatbot.py
   ```

5. **Interaction**:
   Start asking questions about the content of your PDF document.

## Future Enhancements

- Multi-document support for simultaneous querying across multiple PDFs.
- Integration of a web interface for easier interaction.
- Implementation of active learning to improve response quality over time.
- Support for additional document formats beyond PDF.

