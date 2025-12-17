"""
ReAct Agent Demo

Demonstrates the ReAct (Reasoning + Acting) pattern for transparent agent behavior.
"""

import os
from google import genai

def search(query: str) -> str:
    """Search for information.
    
    Args:
        query: Search query
    
    Returns:
        Simulated search results
    """
    # Simulate search results
    results = {
        "python": "Python is a high-level programming language created by Guido van Rossum in 1991.",
        "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "gemini": "Gemini is Google's family of multimodal AI models.",
    }
    
    for key in results:
        if key in query.lower():
            return results[key]
    
    return f"Search results for '{query}': Information about {query}"

def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    
    Args:
        expression: Math expression to evaluate
    
    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"

def main():
    # Initialize client
    client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))
    
    # ReAct system instruction
    system_instruction = """You are a ReAct agent that follows this pattern:

For each step:
1. Thought: Explain your reasoning about what to do next
2. Action: Choose a tool to use (search or calculate)
3. Observation: Analyze the result from the action

Continue this loop until you can provide a final answer.

Available tools:
- search(query): Search for information
- calculate(expression): Perform calculations

Format your response showing Thought, Action, and Observation for each step.
When ready to answer, state your final answer clearly.
"""
    
    # Create agent
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "tools": [search, calculate],
            "system_instruction": system_instruction
        }
    )
    
    print("ReAct Agent started. Type 'exit' to quit.\n")
    print("Try asking:")
    print("  - What is Python and how popular is it?")
    print("  - Calculate 15 * 24 + 100")
    print("  - Tell me about Gemini\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Agent: Goodbye!")
            break
        
        if not user_input.strip():
            continue
        
        try:
            print("\nAgent thinking...\n")
            response = chat.send_message(user_input)
            print(f"Agent: {response.text}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
