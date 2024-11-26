import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from chat_base.core.chat import Chat

def main():
    # Initialize with OpenAI
    openai_chat = Chat(service_provider='openai')
    
    # Get a simple response
    response = openai_chat.get_response(
        message="What is the capital of France?",
        temperature=0.7
    )
    print("OpenAI Response:", response)
    
    # Use Claude with a system prompt
    claude_chat = Chat(service_provider='claude')
    claude_chat.set_system_prompt(
        "You are a helpful assistant that specializes in geography."
    )
    
    response = claude_chat.get_response(
        message="What are the top 3 largest cities in Japan?",
        temperature=0.7
    )
    print("\nClaude Response:", response)
    
    # Use chat completion with multiple messages
    messages = [
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
    ]
    
    response = openai_chat.get_chat_completion(
        messages=messages,
        temperature=0.7
    )
    print("\nChat Completion Response:", response)

if __name__ == "__main__":
    main()
