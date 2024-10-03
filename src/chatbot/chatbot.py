import openai
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from knowledge_base import KnowledgeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(query, knowledge_base, conversation_history, persistent_summary):
    # Perform semantic search to find the most relevant chunks from the knowledge base
    top_chunks = knowledge_base.search(query, top_n=3)
    
    # Combine the persistent summary, conversation history, and knowledge base context
    context = f"Persistent Summary: {persistent_summary}\n\n"
    context += "\n".join(conversation_history[-5:]) + "\n\n"  # Include the last 5 interactions only
    context += "Knowledge Base Context:\n" + "\n".join(top_chunks)

    # Generate a response using the context
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant that uses the given context to provide accurate responses."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def summarize_history(conversation_history):
    # Create a prompt to summarize the conversation with focus on key points and examples
    prompt = f"Summarize the following conversation, focusing on key points and examples:\n\n{'\n'.join(conversation_history)}\n\nComprehensive Summary:"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"

def update_persistent_summary(persistent_summary, new_summary):
    # Combine the old persistent summary with the new summary while avoiding redundancy
    prompt = f"Update the persistent summary with the new information while avoiding redundancy:\n\nCurrent Summary: {persistent_summary}\n\nNew Information: {new_summary}\n\nUpdated Summary:"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred during summarizing persistent information: {str(e)}"

def run_chatbot(embedding_file_path):
    # Initialize the knowledge base
    knowledge_base = KnowledgeBase(embedding_file_path)
    
    # Initialize conversation history and persistent summary
    conversation_history = []
    persistent_summary = "This is a knowledgeable chatbot"

    # Chat loop
    print("Chatbot is ready! Ask a question related to the Flutter Dart (type 'exit' to quit):")
    while True:
        try:
            user_query = input("\nYou: ").strip()
            if user_query.lower() == 'exit':
                break
            
            # Summarize the conversation if it becomes too long
            if len(conversation_history) > 15:  # Adjust this limit as needed
                new_summary = summarize_history(conversation_history)
                persistent_summary = update_persistent_summary(persistent_summary, new_summary)
                conversation_history = [f"Summary: {new_summary}"]  # Reset history with the new summary
                print("Conversation history summarized and added to the persistent summary.")

            # Generate response
            response = generate_response(user_query, knowledge_base, conversation_history, persistent_summary)
            
            # Add the new conversation turn to the history
            conversation_history.append(f"You: {user_query}")
            conversation_history.append(f"Chatbot: {response}")
            
            print(f"Chatbot: {response}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    # This block is for testing the chatbot directly
    embedding_file_path = 'path/to/your/embedding/file.json'
    run_chatbot(embedding_file_path)