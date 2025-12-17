"""
Simple AI Agent Example

A basic conversational agent that maintains context across multiple turns.
"""

import os
from google import genai

def main():
    # Initialize client
    client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))
    
    # Create chat session with system instruction
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": """You are a helpful AI assistant.
            Provide clear, concise answers and maintain context throughout the conversation.
            """
        }
    )
    
    print("Simple Agent started. Type 'exit' to quit.\n")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Agent: Goodbye!")
            break
        
        if not user_input.strip():
            continue
        
        # Get response
        try:
            response = chat.send_message(user_input)
            print(f"Agent: {response.text}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
