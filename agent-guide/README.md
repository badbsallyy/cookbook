# Gemini Agent Development Guide

Welcome to the comprehensive guide for building AI agents with the Gemini API. This guide focuses on practical, production-ready patterns for agent development.

## 🎯 What You'll Learn

This guide covers everything needed to build intelligent agents:
- **Setup & Configuration** - Get started quickly
- **Core Concepts** - Master prompting, streaming, and structured outputs
- **Tools & Capabilities** - Function calling, code execution, file processing
- **Workflows & Patterns** - ReAct, chaining, multi-turn conversations
- **Real Examples** - Working code you can use immediately

## 📚 Guide Structure

### [Setup](setup/)
Get your development environment ready:
- **[Installation](setup/installation.md)** - Python environment and dependencies
- **[Authentication](setup/authentication.md)** - API key setup and security
- **[Configuration](setup/configuration.md)** - Model selection and parameters

### [Core](core/)
Master the fundamentals:
- **[Prompting](core/prompting.md)** - Effective prompt engineering and system instructions
- **[Streaming](core/streaming.md)** - Real-time response streaming
- **[JSON Mode](core/json-mode.md)** - Structured outputs for data extraction
- **[Error Handling](core/error-handling.md)** - Robust error management
- **[Models](core/models.md)** - Choosing and using Gemini models

### [Tools](tools/)
Add capabilities to your agents:
- **[Function Calling](tools/function-calling.md)** - Connect agents to external tools and APIs
- **[Code Execution](tools/code-execution.md)** - Execute Python code for calculations and analysis
- **[File API](tools/file-api.md)** - Process documents, images, audio, and video
- **[Search & Grounding](tools/search-grounding.md)** - Access real-time information with Google Search

### [Workflows](workflows/)
Build sophisticated agent patterns:
- **[ReAct Pattern](workflows/react-pattern.md)** - Reasoning + Acting for transparent decision-making
- **[Prompt Chaining](workflows/chaining.md)** - Break complex tasks into steps
- **[Multi-Turn Conversations](workflows/multi-turn.md)** - Build stateful conversational agents

### [Examples](examples/)
Learn from working code:
- **[Agent Examples](examples/agent-examples.md)** - Complete agent implementations
- **[Code Samples](examples/code/)** - Python scripts you can run

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install google-genai
```

### 2. Set API Key

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 3. Run Your First Agent

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello! Help me understand AI agents."
)

print(response.text)
```

## 💡 Common Use Cases

### Simple Q&A Agent
```python
chat = client.chats.create(model="gemini-2.5-flash")
response = chat.send_message("What is machine learning?")
```

### Agent with Tools
```python
def search(query: str) -> str:
    return f"Results for: {query}"

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={"tools": [search]}
)
response = chat.send_message("Search for Python tutorials")
```

### Data Analysis Agent
```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Calculate the average of: 10, 20, 30, 40, 50",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)
```

## 🎨 Agent Patterns

### ReAct Agent (Recommended)
Best for: Complex reasoning tasks, transparent decision-making

```python
system_instruction = """You are a ReAct agent.
For each step:
1. Thought: Reason about what to do
2. Action: Use a tool
3. Observation: Analyze the result
"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [search, calculate],
        "system_instruction": system_instruction
    }
)
```

### Conversational Agent
Best for: Customer service, personal assistants

```python
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": "You are a helpful customer service agent."
    }
)

# Maintains context across turns
response1 = chat.send_message("I have a problem with my order")
response2 = chat.send_message("The order number is 12345")
```

### Data Processing Agent
Best for: Analysis, extraction, transformation

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Extract names and emails from this text: ...",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "people": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    }
                }
            }
        }
    )
)
```

## 🛠️ Recommended Models

| Use Case | Model | Why |
|----------|-------|-----|
| General agents | `gemini-2.5-flash` | Best balance of speed, capability, cost |
| High-volume tasks | `gemini-2.5-flash-lite` | Fastest, most cost-effective |
| Complex reasoning | `gemini-2.5-pro` | Best for sophisticated analysis |
| Experiments | `gemini-3-pro-preview` | Latest capabilities |

## 📋 Best Practices

### 1. System Instructions
Always set clear system instructions:
```python
system_instruction = """You are a [role].
Your capabilities: [list]
Your limitations: [list]
Output format: [specification]
"""
```

### 2. Error Handling
Implement robust error handling:
```python
try:
    response = client.models.generate_content(...)
except exceptions.ResourceExhausted:
    # Handle rate limiting
    time.sleep(60)
except exceptions.InvalidArgument:
    # Handle bad input
    pass
```

### 3. Tool Design
Design focused, single-purpose tools:
```python
def search(query: str) -> str:
    """Search for information.
    
    Args:
        query: Specific search query
    
    Returns:
        Search results as string
    """
    # Implementation
```

### 4. Response Validation
Validate structured outputs:
```python
import json

response = client.models.generate_content(
    ...,
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

try:
    data = json.loads(response.text)
    # Validate schema
except json.JSONDecodeError:
    # Handle invalid JSON
    pass
```

## 🔍 Common Patterns

### Sequential Tasks
```python
# Step 1: Research
research = client.models.generate_content(...).text

# Step 2: Analyze
analysis = client.models.generate_content(
    contents=f"Analyze: {research}"
).text

# Step 3: Summarize
summary = client.models.generate_content(
    contents=f"Summarize: {analysis}"
).text
```

### Parallel Tasks
```python
from concurrent.futures import ThreadPoolExecutor

def process_item(item):
    return client.models.generate_content(
        contents=f"Process: {item}"
    ).text

with ThreadPoolExecutor() as executor:
    results = list(executor.map(process_item, items))
```

### Iterative Refinement
```python
content = initial_draft

for i in range(3):
    content = client.models.generate_content(
        contents=f"Improve this: {content}"
    ).text
```

## 📖 Learning Path

### Beginner
1. [Installation](setup/installation.md) → [Authentication](setup/authentication.md)
2. [Prompting Basics](core/prompting.md)
3. [Simple Agent](examples/code/simple_agent.py)

### Intermediate
1. [Function Calling](tools/function-calling.md)
2. [JSON Mode](core/json-mode.md)
3. [Multi-Turn Conversations](workflows/multi-turn.md)

### Advanced
1. [ReAct Pattern](workflows/react-pattern.md)
2. [Prompt Chaining](workflows/chaining.md)
3. [Production Error Handling](core/error-handling.md)

## 🤝 Contributing

Found an issue or want to improve this guide? Please see the main repository [CONTRIBUTING.md](../CONTRIBUTING.md).

## 📝 License

See [LICENSE](../LICENSE) for details.

## 🔗 Additional Resources

- [Official Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Python SDK Reference](https://github.com/googleapis/python-genai)
- [Google AI Studio](https://aistudio.google.com/)
- [Developer Forum](https://discuss.ai.google.dev/)

## 🎯 Next Steps

Ready to start building? Jump to:
- **New to Gemini?** → [Installation Guide](setup/installation.md)
- **Building first agent?** → [Function Calling](tools/function-calling.md)
- **Need patterns?** → [ReAct Pattern](workflows/react-pattern.md)
- **Looking for examples?** → [Agent Examples](examples/agent-examples.md)

---

**Need help?** Check the [Official Documentation](https://ai.google.dev/gemini-api/docs) or ask on the [Developer Forum](https://discuss.ai.google.dev/).
