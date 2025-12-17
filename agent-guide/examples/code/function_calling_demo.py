"""
Function Calling Demo

Demonstrates how to give an agent access to tools/functions.
"""

import os
from google import genai
from datetime import datetime

def get_current_time() -> str:
    """Get the current time.
    
    Returns:
        Current time as a formatted string
    """
    return datetime.now().strftime("%H:%M:%S")

def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
    
    Returns:
        Result of the calculation
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def search_info(query: str) -> str:
    """Search for information (simulated).
    
    Args:
        query: Search query
    
    Returns:
        Simulated search results
    """
    # In a real implementation, this would call an actual search API
    return f"Search results for '{query}': [Relevant information would appear here]"

def main():
    # Initialize client
    client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))
    
    # Create chat with tools
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "tools": [get_current_time, calculate, search_info],
            "system_instruction": """You are an AI assistant with access to tools:
            - get_current_time(): Get current time
            - calculate(expression): Perform calculations
            - search_info(query): Search for information
            
            Use these tools when appropriate to help the user.
            """
        }
    )
    
    print("Function Calling Agent started. Type 'exit' to quit.\n")
    print("Try asking:")
    print("  - What time is it?")
    print("  - What is 15 * 24?")
    print("  - Search for Python tutorials\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Agent: Goodbye!")
            break
        
        if not user_input.strip():
            continue
        
        try:
            response = chat.send_message(user_input)
            print(f"Agent: {response.text}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
