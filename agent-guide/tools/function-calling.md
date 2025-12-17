# Function Calling

## Overview

Function calling enables Gemini models to use external tools and APIs. This is essential for building agents that can interact with the real world, databases, APIs, and other systems.

## How It Works

1. **Define functions** with clear names, descriptions, and parameters
2. **Pass functions to model** as available tools
3. **Model decides** when to call functions based on user intent
4. **Execute functions** in your code
5. **Return results** to model
6. **Model uses results** to generate final response

## Basic Function Calling

### Simple Example

```python
from google import genai
from google.genai import types

client = genai.Client()

# Define a function
def get_weather(location: str) -> dict:
    """Get weather information for a location.
    
    Args:
        location: City name or location
    """
    # Simulate weather API call
    return {
        "location": location,
        "temperature": 72,
        "condition": "sunny"
    }

# Create tools list
tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_weather",
                description="Get current weather for a location",
                parameters={
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        }
                    },
                    "required": ["location"]
                }
            )
        ]
    )
]

# Call model with tools
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What's the weather in San Francisco?",
    config=types.GenerateContentConfig(
        tools=tools
    )
)

# Check if model wants to call function
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function: {function_call.name}")
    print(f"Arguments: {function_call.args}")
```

## Using Python Functions Directly

### Auto-Declaration

```python
def enable_lights():
    """Turn on the lighting system."""
    print("Lights enabled")
    return {"status": "on"}

def set_light_color(rgb_hex: str):
    """Set light color.
    
    Args:
        rgb_hex: Color in hex format (e.g., '#FF0000')
    """
    print(f"Color set to {rgb_hex}")
    return {"color": rgb_hex}

# Pass functions directly - SDK extracts schema from annotations
tools = [enable_lights, set_light_color]

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": tools,
        "system_instruction": "You control a lighting system"
    }
)

response = chat.send_message("Turn on the lights and set them to red")
print(response.text)
```

## Manual Function Execution

### Step-by-Step Control

```python
def search(query: str) -> str:
    """Search for information.
    
    Args:
        query: Search query
    """
    return f"Results for: {query}"

# Define tool
tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search",
                description="Search for information online",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        }
                    },
                    "required": ["query"]
                }
            )
        ]
    )
]

# First request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Find information about quantum computing",
    config=types.GenerateContentConfig(
        tools=tools
    )
)

# Check for function call
if response.candidates[0].content.parts[0].function_call:
    func_call = response.candidates[0].content.parts[0].function_call
    
    # Execute function
    if func_call.name == "search":
        result = search(**func_call.args)
        
        # Send result back to model
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {"role": "user", "parts": [{"text": "Find information about quantum computing"}]},
                {"role": "model", "parts": [{"function_call": func_call}]},
                {"role": "user", "parts": [{
                    "function_response": {
                        "name": func_call.name,
                        "response": {"result": result}
                    }
                }]}
            ],
            config=types.GenerateContentConfig(
                tools=tools
            )
        )
        
        print(response.text)
```

## Automatic Function Execution

### Chat Session with Auto-Execution

```python
# Define functions
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression.
    
    Args:
        expression: Math expression to evaluate
    """
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"

def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

# Create chat with automatic function calling
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [calculate, get_time],
        "system_instruction": "You are a helpful assistant with access to calculation and time tools"
    }
)

# Automatic execution enabled by default
response = chat.send_message("What time is it? And what's 15 * 24?")
print(response.text)
```

## Multiple Functions

### Complete Agent Example

```python
from datetime import datetime
import json

# Define multiple tools
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for '{query}': [sample results]"

def save_note(content: str) -> str:
    """Save a note."""
    return f"Note saved: {content[:50]}..."

def get_date() -> str:
    """Get current date."""
    return datetime.now().strftime("%Y-%m-%d")

def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression)

# Create agent
tools = [search_web, save_note, get_date, calculate]

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": tools,
        "system_instruction": """You are a helpful AI assistant with access to:
        - Web search
        - Note taking
        - Date/time information
        - Calculator
        
        Use these tools when needed to help the user."""
    }
)

# Multi-step interaction
response = chat.send_message(
    "Search for Python tutorials, then save a note with today's date"
)
print(response.text)
```

## Advanced Function Schemas

### Complex Parameters

```python
# Function with complex parameters
tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="create_task",
            description="Create a task with details",
            parameters={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Task priority"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in YYYY-MM-DD format"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of tags"
                    },
                    "assignee": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    }
                },
                "required": ["title", "priority"]
            }
        )
    ]
)
```

### Nested Objects

```python
tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="process_order",
            description="Process an order",
            parameters={
                "type": "object",
                "properties": {
                    "customer": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "address": {
                                "type": "object",
                                "properties": {
                                    "street": {"type": "string"},
                                    "city": {"type": "string"},
                                    "zip": {"type": "string"}
                                }
                            }
                        }
                    },
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "string"},
                                "quantity": {"type": "integer"}
                            }
                        }
                    }
                },
                "required": ["customer", "items"]
            }
        )
    ]
)
```

## Function Calling Patterns

### Sequential Tool Use

```python
def fetch_data(source: str) -> dict:
    """Fetch data from a source."""
    return {"data": f"Data from {source}"}

def analyze_data(data: dict) -> str:
    """Analyze data."""
    return f"Analysis of {data}"

def generate_report(analysis: str) -> str:
    """Generate a report."""
    return f"Report: {analysis}"

# Chain tools together
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [fetch_data, analyze_data, generate_report],
        "system_instruction": "Complete tasks step by step using available tools"
    }
)

response = chat.send_message(
    "Fetch data from database, analyze it, and generate a report"
)
```

### Parallel Tool Use

```python
def check_weather(location: str) -> dict:
    """Check weather."""
    return {"temp": 72, "condition": "sunny"}

def check_traffic(location: str) -> dict:
    """Check traffic."""
    return {"status": "light", "delay": 5}

def check_calendar(date: str) -> list:
    """Check calendar."""
    return ["Meeting at 10am", "Lunch at 12pm"]

# Model can request multiple functions at once
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [check_weather, check_traffic, check_calendar]
    }
)

response = chat.send_message(
    "Check the weather, traffic, and my calendar for today"
)
```

## Error Handling

### Safe Function Execution

```python
def safe_execute_function(func_name, func_args, available_functions):
    """Safely execute a function with error handling."""
    
    try:
        if func_name not in available_functions:
            return {"error": f"Function {func_name} not found"}
        
        func = available_functions[func_name]
        result = func(**func_args)
        return {"success": True, "result": result}
        
    except TypeError as e:
        return {"error": f"Invalid arguments: {e}"}
    except Exception as e:
        return {"error": f"Execution failed: {e}"}

# Usage
available_functions = {
    "search": search_web,
    "calculate": calculate
}

# Execute function call from model
if function_call:
    result = safe_execute_function(
        function_call.name,
        function_call.args,
        available_functions
    )
    
    if "error" in result:
        print(f"Error: {result['error']}")
```

### Retry Logic

```python
def execute_with_retry(func, args, max_retries=3):
    """Execute function with retry logic."""
    
    for attempt in range(max_retries):
        try:
            return func(**args)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(1)
            else:
                return {"error": f"Failed after {max_retries} attempts: {e}"}
```

## Best Practices

1. **Clear function names**: Use descriptive, action-oriented names
2. **Detailed descriptions**: Explain what the function does and when to use it
3. **Type hints**: Always include parameter types
4. **Required parameters**: Mark mandatory parameters
5. **Error handling**: Return errors as structured data
6. **Validation**: Validate function inputs before execution
7. **Documentation**: Add docstrings to all functions
8. **Testing**: Test functions independently before integration

## ReAct Agent with Tools

```python
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"

def calculate(expression: str) -> float:
    """Calculate mathematical expression."""
    return eval(expression)

system_instruction = """You are a ReAct agent. For each task:

1. Thought: Reason about what to do next
2. Action: Choose a tool to use
3. Observation: Analyze the result
4. Repeat until done

Available tools:
- search: Find information
- calculate: Do math

Format your response as:
Thought: [your reasoning]
Action: [tool to use]
Observation: [what you learned]
"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [search, calculate],
        "system_instruction": system_instruction
    }
)

response = chat.send_message(
    "What is the population of Tokyo multiplied by 1.5?"
)
print(response.text)
```

## Next Steps

- [Code Execution](code-execution.md) - Run Python code directly
- [File API](file-api.md) - Work with files
- [Search & Grounding](search-grounding.md) - Use Google Search
- [ReAct Pattern](../workflows/react-pattern.md) - Build reasoning agents
