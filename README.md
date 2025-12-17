# Gemini Agent Development Guide

**Building AI Agents with the Gemini API**

This repository provides a comprehensive, practical guide for building production-ready AI agents using the Gemini API. Focused on agent patterns, workflows, and best practices.

**For comprehensive API documentation, visit [ai.google.dev](https://ai.google.dev/gemini-api/docs).**

---

## 🚀 Quick Start

Jump directly to the **[Agent Guide](./agent-guide/)** for:
- Step-by-step tutorials
- Working code examples
- Production-ready patterns
- Best practices

Or explore:
- **[Setup](./agent-guide/setup/)** - Get started with installation and authentication
- **[Core Concepts](./agent-guide/core/)** - Master prompting, streaming, and structured outputs
- **[Tools](./agent-guide/tools/)** - Add function calling, code execution, and search
- **[Workflows](./agent-guide/workflows/)** - Learn ReAct, chaining, and multi-turn patterns
- **[Examples](./agent-guide/examples/)** - Ready-to-run agent code

## 📚 What's in This Guide

### Agent Development Guide
The **[agent-guide/](./agent-guide/)** directory contains everything you need to build AI agents:

**Setup & Configuration**
- Installation and dependencies
- API authentication
- Model configuration

**Core Skills**
- Prompting and system instructions
- Streaming responses
- JSON mode for structured outputs
- Error handling
- Model selection

**Agent Tools**
- Function calling for external APIs
- Code execution for calculations
- File API for documents and media
- Search grounding for real-time information

**Agent Patterns**
- ReAct (Reasoning + Acting) pattern
- Prompt chaining for complex tasks
- Multi-turn conversations

### Legacy Resources
- **[quickstarts/](./quickstarts/)** - Original Jupyter notebooks (see note below)
- **[examples/](./examples/)** - Original example notebooks (see note below)

> **Note**: This repository has been restructured to focus on agent development. The original quickstarts and examples remain available for reference, but the **[agent-guide/](./agent-guide/)** provides a more focused, LLM-friendly format optimized for building agents.

---

## 💡 Featured Agent Patterns

### ReAct Agent (Reasoning + Acting)
Build transparent agents that show their thinking:

```python
from google import genai

client = genai.Client()

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

**[Learn more →](./agent-guide/workflows/react-pattern.md)**

### Function Calling Agent
Connect your agent to external tools:

```python
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={"tools": [search]}
)

response = chat.send_message("Search for Python tutorials")
```

**[Learn more →](./agent-guide/tools/function-calling.md)**

### Data Analysis Agent
Process and analyze data with code execution:

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Calculate statistics for: [100, 120, 115, 140]",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)
```

**[Learn more →](./agent-guide/tools/code-execution.md)**

---

## 🎯 Getting Started

### Installation

```bash
pip install google-genai
```

### Authentication

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Your First Agent

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello! Explain what you can do."
)

print(response.text)
```

**[Full installation guide →](./agent-guide/setup/installation.md)**

---

## 📖 Learning Path

### Beginner
1. **[Installation](./agent-guide/setup/installation.md)** - Set up your environment
2. **[Authentication](./agent-guide/setup/authentication.md)** - Configure API access
3. **[Prompting Basics](./agent-guide/core/prompting.md)** - Learn effective prompting
4. **[Simple Agent Example](./agent-guide/examples/code/simple_agent.py)** - Run your first agent

### Intermediate
1. **[Function Calling](./agent-guide/tools/function-calling.md)** - Add tools to agents
2. **[JSON Mode](./agent-guide/core/json-mode.md)** - Get structured outputs
3. **[Multi-Turn Conversations](./agent-guide/workflows/multi-turn.md)** - Build stateful agents
4. **[Error Handling](./agent-guide/core/error-handling.md)** - Handle failures gracefully

### Advanced
1. **[ReAct Pattern](./agent-guide/workflows/react-pattern.md)** - Build reasoning agents
2. **[Prompt Chaining](./agent-guide/workflows/chaining.md)** - Complex multi-step workflows
3. **[Code Execution](./agent-guide/tools/code-execution.md)** - Data analysis agents
4. **[Search Grounding](./agent-guide/tools/search-grounding.md)** - Real-time information

---

## 🔧 Tools & Capabilities

| Tool | Description | Guide |
|------|-------------|-------|
| **Function Calling** | Connect to external APIs and tools | [→](./agent-guide/tools/function-calling.md) |
| **Code Execution** | Run Python for calculations and analysis | [→](./agent-guide/tools/code-execution.md) |
| **File API** | Process documents, images, audio, video | [→](./agent-guide/tools/file-api.md) |
| **Search Grounding** | Access real-time web information | [→](./agent-guide/tools/search-grounding.md) |

---

## 🎨 Agent Workflows

| Pattern | Best For | Guide |
|---------|----------|-------|
| **ReAct** | Transparent reasoning, complex tasks | [→](./agent-guide/workflows/react-pattern.md) |
| **Chaining** | Multi-step workflows, refinement | [→](./agent-guide/workflows/chaining.md) |
| **Multi-Turn** | Conversational agents, context retention | [→](./agent-guide/workflows/multi-turn.md) |

---


## 📚 Additional Resources

### Official SDKs

This guide uses Python, but the Gemini API is available in multiple languages:

* **[Python](https://github.com/googleapis/python-genai)** (Recommended for agents)
* [Go](https://github.com/google/generative-ai-go)
* [Node.js](https://github.com/google/generative-ai-js)
* [Dart (Flutter)](https://github.com/google/generative-ai-dart)
* [Android](https://github.com/google/generative-ai-android)
* [Swift](https://github.com/google/generative-ai-swift)

### Documentation

* **[Agent Development Guide](./agent-guide/)** - This repository's main guide
* [Official Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
* [Google AI Studio](https://aistudio.google.com/)
* [Developer Forum](https://discuss.ai.google.dev/)

### Example Applications

* [Gemini CLI](https://github.com/google-gemini/gemini-cli) - AI agent in your terminal
* [Gemini API Quickstart](https://github.com/google-gemini/gemini-api-quickstart) - Flask starter app
* [Multimodal Live API Console](https://github.com/google-gemini/multimodal-live-api-web-console) - React app
* [Fullstack LangGraph](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart) - Complete stack

### Enterprise

For enterprise developers, Gemini is also available on **Google Cloud Vertex AI**. See the [Vertex AI generative AI repository](https://github.com/GoogleCloudPlatform/generative-ai).

---

## 🤝 Contributing

We welcome contributions to improve this guide! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Adding new examples
- Improving documentation
- Reporting issues
- Suggesting new patterns

---

## 📄 License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

---

**Ready to build agents?** Start with the **[Agent Development Guide](./agent-guide/)** or jump straight to **[Examples](./agent-guide/examples/)**.

Questions? Visit the [Developer Forum](https://discuss.ai.google.dev/) or check the [Official Documentation](https://ai.google.dev/gemini-api/docs).




