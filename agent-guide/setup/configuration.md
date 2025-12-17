# Configuration

## Overview

This guide covers configuring the Gemini API client for optimal agent development.

## Client Initialization

### Basic Configuration

```python
from google import genai

# Initialize with explicit API key
client = genai.Client(api_key="YOUR_API_KEY")

# Initialize with environment variable
import os
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# Initialize with automatic key detection
client = genai.Client()
```

## Model Selection

Choose the appropriate model for your use case:

```python
# Fast and efficient for most tasks
model = "gemini-2.5-flash"

# Most capable model for complex reasoning
model = "gemini-2.5-pro"

# Latest preview with advanced capabilities
model = "gemini-3-pro-preview"

# Lightweight model for simple tasks
model = "gemini-2.5-flash-lite"
```

### Model Comparison

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| gemini-2.5-flash-lite | Simple queries, high volume | Fastest | Lowest |
| gemini-2.5-flash | General purpose, agents | Fast | Low |
| gemini-2.5-pro | Complex reasoning | Moderate | Moderate |
| gemini-3-pro-preview | Cutting edge features | Variable | Higher |

## Generation Configuration

### Basic Parameters

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt here",
    config={
        "temperature": 0.7,        # Controls randomness (0.0-2.0)
        "top_p": 0.95,            # Nucleus sampling
        "top_k": 40,              # Top-k sampling
        "max_output_tokens": 2048, # Maximum response length
        "stop_sequences": ["END"]  # Sequences to stop generation
    }
)
```

### Temperature Settings

- **0.0-0.3**: Deterministic, focused outputs (good for code, facts)
- **0.4-0.7**: Balanced creativity and consistency (good for agents)
- **0.8-1.5**: Creative, diverse outputs (good for content generation)
- **1.6-2.0**: Highly random outputs (experimental)

## Safety Settings

Configure content filtering:

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt here",
    config={
        "safety_settings": [
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_MEDIUM_AND_ABOVE"
            ),
        ]
    }
)
```

Threshold options:
- `BLOCK_NONE`: No filtering
- `BLOCK_ONLY_HIGH`: Block only high-risk content
- `BLOCK_MEDIUM_AND_ABOVE`: Block medium and high-risk content
- `BLOCK_LOW_AND_ABOVE`: Block most content (strictest)

## System Instructions

Set persistent instructions for the model:

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="User query here",
    config={
        "system_instruction": """You are a helpful assistant that:
        - Provides concise, accurate answers
        - Uses bullet points when appropriate
        - Cites sources when making factual claims
        - Admits when you don't know something
        """
    }
)
```

## Response Configuration

### JSON Mode

Request structured JSON responses:

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Extract key information from: [text here]",
    config={
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "key_points": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    }
)
```

## Timeout and Retry Configuration

```python
from google.api_core import retry

# Configure retry behavior
retry_policy = retry.Retry(
    initial=1.0,      # Initial delay (seconds)
    maximum=60.0,     # Maximum delay (seconds)
    multiplier=2.0,   # Backoff multiplier
    timeout=300.0     # Total timeout (seconds)
)

# Use with client (implementation-specific)
```

## Environment-Specific Configuration

### Development

```python
config = {
    "temperature": 0.9,
    "max_output_tokens": 1024,
}
```

### Production

```python
config = {
    "temperature": 0.4,
    "max_output_tokens": 2048,
    "safety_settings": [
        # Strict safety settings
    ]
}
```

## Configuration Best Practices

1. **Use environment variables** for API keys and sensitive data
2. **Set appropriate temperature** based on task (lower for deterministic, higher for creative)
3. **Configure safety settings** based on your application's needs
4. **Set reasonable token limits** to control costs
5. **Use system instructions** to establish consistent behavior
6. **Test configurations** with sample inputs before production

## Configuration File Example

Create a `config.py` file:

```python
import os
from google.genai import types

# API Configuration
API_KEY = os.environ.get('GOOGLE_API_KEY')
DEFAULT_MODEL = "gemini-2.5-flash"

# Generation Configuration
DEFAULT_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# Agent System Instruction
AGENT_SYSTEM_INSTRUCTION = """You are an AI agent that:
- Breaks down complex tasks into steps
- Uses available tools when needed
- Provides clear, actionable responses
- Explains your reasoning
"""

# Safety Settings
SAFETY_SETTINGS = [
    types.SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="BLOCK_MEDIUM_AND_ABOVE"
    ),
    # Add other categories...
]
```

## Next Steps

- [Prompting Guide](../core/prompting.md) - Learn effective prompting techniques
- [Function Calling](../tools/function-calling.md) - Add tools to your agents
- [Error Handling](../core/error-handling.md) - Handle API errors gracefully
