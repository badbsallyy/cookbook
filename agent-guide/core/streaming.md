# Streaming API

## Overview

Streaming allows your agent to receive responses incrementally as they're generated, rather than waiting for the complete response. This provides a better user experience for long-running queries.

## Basic Streaming

### Simple Stream Example

```python
from google import genai

client = genai.Client()

prompt = "Write a detailed explanation of how neural networks work"

# Stream the response
for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=prompt
):
    print(chunk.text, end="")
```

### With Configuration

```python
from google.genai import types

for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=2048
    )
):
    if chunk.text:
        print(chunk.text, end="", flush=True)
```

## Handling Stream Chunks

### Process Each Chunk

```python
full_response = ""

for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Explain quantum computing"
):
    chunk_text = chunk.text
    full_response += chunk_text
    
    # Process each chunk
    print(chunk_text, end="", flush=True)

print(f"\n\nTotal length: {len(full_response)} characters")
```

### With Metadata

```python
for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=prompt
):
    # Access metadata
    if hasattr(chunk, 'usage_metadata'):
        print(f"Tokens used: {chunk.usage_metadata.total_token_count}")
    
    # Access text
    if chunk.text:
        print(chunk.text, end="")
```

## Agent Use Cases

### Interactive Agent Response

```python
def agent_stream_response(user_query, system_instruction):
    """Stream an agent response with thinking process"""
    
    print("Agent: ", end="", flush=True)
    
    full_response = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.4
        )
    ):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text
    
    print()  # New line
    return full_response

# Usage
system_inst = """You are a helpful agent. 
Show your thinking process step by step."""

response = agent_stream_response(
    "How do I deploy a Python app to production?",
    system_inst
)
```

### Progress Indicator

```python
import sys
import time

def stream_with_progress(prompt):
    """Stream response with progress indicator"""
    
    chars_received = 0
    start_time = time.time()
    
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt
    ):
        if chunk.text:
            chars_received += len(chunk.text)
            elapsed = time.time() - start_time
            
            # Show progress
            sys.stdout.write(f"\rReceived: {chars_received} chars in {elapsed:.1f}s")
            sys.stdout.flush()
    
    print()  # New line after progress

# Usage
stream_with_progress("Explain machine learning in detail")
```

## Error Handling

### Basic Error Handling

```python
from google.api_core import exceptions

try:
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt
    ):
        print(chunk.text, end="")
        
except exceptions.GoogleAPIError as e:
    print(f"\nAPI Error: {e}")
except Exception as e:
    print(f"\nUnexpected error: {e}")
```

### Retry on Errors

```python
import time

def stream_with_retry(prompt, max_retries=3):
    """Stream with automatic retry on failures"""
    
    for attempt in range(max_retries):
        try:
            full_response = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=prompt
            ):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
            
            return full_response
            
        except exceptions.GoogleAPIError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"\nRetrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

# Usage
response = stream_with_retry("Your prompt here")
```

## Multi-Turn Streaming

### Conversational Agent

```python
def streaming_conversation():
    """Handle multi-turn conversation with streaming"""
    
    messages = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # Add user message
        messages.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })
        
        # Stream response
        print("Agent: ", end="", flush=True)
        full_response = ""
        
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=messages
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text
        
        print()  # New line
        
        # Add assistant response to history
        messages.append({
            "role": "model",
            "parts": [{"text": full_response}]
        })

# Usage
streaming_conversation()
```

## Advanced Patterns

### Buffered Streaming

```python
def buffered_stream(prompt, buffer_size=50):
    """Stream in buffered chunks for better control"""
    
    buffer = ""
    
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt
    ):
        if chunk.text:
            buffer += chunk.text
            
            # Flush buffer when it reaches size
            if len(buffer) >= buffer_size:
                print(buffer, end="", flush=True)
                buffer = ""
    
    # Flush remaining buffer
    if buffer:
        print(buffer, end="", flush=True)

# Usage
buffered_stream("Explain AI agents", buffer_size=100)
```

### Real-Time Processing

```python
def process_stream_realtime(prompt, processor_func):
    """Process each chunk in real-time"""
    
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt
    ):
        if chunk.text:
            # Process chunk immediately
            processed = processor_func(chunk.text)
            print(processed, end="", flush=True)

# Example processor
def highlight_keywords(text):
    """Highlight important keywords"""
    keywords = ['important', 'critical', 'note']
    for keyword in keywords:
        text = text.replace(keyword, f"**{keyword}**")
    return text

# Usage
process_stream_realtime(
    "Explain important concepts in AI",
    highlight_keywords
)
```

## Streaming with Function Calling

```python
from google.genai import types

tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search",
                description="Search for information",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    }
                }
            )
        ]
    )
]

for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Search for the latest AI news",
    config=types.GenerateContentConfig(
        tools=tools
    )
):
    # Check for function calls
    if chunk.candidates and chunk.candidates[0].content.parts:
        for part in chunk.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                print(f"\nFunction called: {part.function_call.name}")
                print(f"Arguments: {part.function_call.args}")
            elif hasattr(part, 'text'):
                print(part.text, end="", flush=True)
```

## Performance Optimization

### Concurrent Streams

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def stream_query(query):
    """Stream a single query"""
    result = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=query
    ):
        if chunk.text:
            result += chunk.text
    return result

# Process multiple queries concurrently
queries = [
    "Explain machine learning",
    "Explain neural networks",
    "Explain deep learning"
]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(stream_query, queries))

for i, result in enumerate(results):
    print(f"\n--- Query {i+1} Result ---")
    print(result[:200] + "...")
```

## Best Practices

1. **Always flush output**: Use `flush=True` for real-time display
2. **Handle partial chunks**: Text may arrive in small pieces
3. **Implement timeouts**: Prevent hanging on slow streams
4. **Buffer appropriately**: Balance responsiveness and efficiency
5. **Error handling**: Always wrap streams in try-except
6. **Clean up resources**: Ensure streams are properly closed

## Common Patterns

### Word-by-Word Display

```python
def display_word_by_word(prompt, delay=0.05):
    """Display words with slight delay for effect"""
    import time
    
    buffer = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt
    ):
        if chunk.text:
            buffer += chunk.text
            words = buffer.split()
            
            for word in words[:-1]:
                print(word, end=" ", flush=True)
                time.sleep(delay)
            
            # Keep last partial word in buffer
            buffer = words[-1] if words else ""
    
    # Print remaining
    if buffer:
        print(buffer, flush=True)
```

### Save While Streaming

```python
def stream_and_save(prompt, filename):
    """Stream to console and save to file simultaneously"""
    
    with open(filename, 'w') as f:
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=prompt
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                f.write(chunk.text)
                f.flush()  # Flush to disk

# Usage
stream_and_save(
    "Write a detailed article about AI",
    "/tmp/article.txt"
)
```

## Next Steps

- [JSON Mode](json-mode.md) - Get structured outputs
- [Error Handling](error-handling.md) - Handle errors gracefully
- [Function Calling](../tools/function-calling.md) - Add tools to streams
