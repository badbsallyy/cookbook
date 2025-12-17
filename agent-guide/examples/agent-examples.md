# Agent Examples

This guide provides complete, working examples of different agent types you can build with the Gemini API.

## Running the Examples

All Python examples are in the [`code/`](code/) directory. To run them:

```bash
# Set your API key
export GOOGLE_API_KEY="your_api_key_here"

# Run an example
python agent-guide/examples/code/simple_agent.py
```

## Example Agents

### 1. Simple Conversational Agent

**File:** [`simple_agent.py`](code/simple_agent.py)

A basic agent that maintains conversational context.

**Features:**
- Multi-turn conversation
- Context retention
- Simple error handling

**Use Cases:**
- Customer support
- General Q&A
- Personal assistants

**Code Snippet:**
```python
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": "You are a helpful AI assistant."
    }
)

response = chat.send_message(user_input)
```

### 2. Function Calling Agent

**File:** [`function_calling_demo.py`](code/function_calling_demo.py)

An agent with access to external tools and functions.

**Features:**
- Multiple tools (time, calculator, search)
- Automatic tool selection
- Tool execution handling

**Use Cases:**
- Task automation
- Information retrieval
- API integration

**Code Snippet:**
```python
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    return str(eval(expression))

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [get_time, calculate, search],
        "system_instruction": "Use tools to help the user."
    }
)
```

### 3. ReAct Agent

**File:** [`react_agent_demo.py`](code/react_agent_demo.py)

An agent that shows its reasoning process.

**Features:**
- Transparent decision-making
- Step-by-step reasoning
- Tool selection with explanation

**Use Cases:**
- Complex problem solving
- Educational applications
- Debugging and analysis

**Code Snippet:**
```python
system_instruction = """You are a ReAct agent.

For each step:
1. Thought: Explain your reasoning
2. Action: Choose a tool
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

## Additional Examples

### Research Agent

```python
from google import genai
from google.genai import types

client = genai.Client()

system_instruction = """You are a research assistant.
Use Google Search to find accurate, current information.
Always cite your sources."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(google_search={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message("What are the latest AI trends in 2025?")
print(response.text)
```

### Data Analysis Agent

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""Analyze this data and provide insights:

Sales: [100, 120, 115, 140, 135, 150, 145]

Calculate:
- Average
- Trend
- Growth rate
""",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

print(response.text)
```

### Document Processing Agent

```python
from google import genai

client = genai.Client()

# Upload document
uploaded_file = client.files.upload(path="document.pdf")

# Process document
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        uploaded_file,
        "Summarize this document and extract key points"
    ]
)

print(response.text)

# Cleanup
client.files.delete(name=uploaded_file.name)
```

### Multi-Agent System

```python
class MultiAgentSystem:
    """Coordinate multiple specialized agents."""
    
    def __init__(self):
        self.client = genai.Client()
        
        # Researcher agent
        self.researcher = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "tools": [types.Tool(google_search={})],
                "system_instruction": "You research topics thoroughly."
            }
        )
        
        # Analyzer agent
        self.analyzer = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "system_instruction": "You analyze and provide insights."
            }
        )
        
        # Writer agent
        self.writer = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "system_instruction": "You write clear, engaging content."
            }
        )
    
    def process(self, topic):
        """Process topic through all agents."""
        
        # Research
        research = self.researcher.send_message(
            f"Research {topic}"
        ).text
        
        # Analyze
        analysis = self.analyzer.send_message(
            f"Analyze this research: {research}"
        ).text
        
        # Write
        article = self.writer.send_message(
            f"Write an article based on: {analysis}"
        ).text
        
        return article

# Usage
system = MultiAgentSystem()
article = system.process("AI in healthcare")
```

## Advanced Patterns

### Agent with Memory

```python
class MemoryAgent:
    """Agent that remembers past interactions."""
    
    def __init__(self):
        self.client = genai.Client()
        self.memory = {}
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash"
        )
    
    def remember(self, key, value):
        """Store information."""
        self.memory[key] = value
    
    def recall(self, key):
        """Retrieve information."""
        return self.memory.get(key)
    
    def send_message(self, message):
        """Send message with memory context."""
        
        # Add memory context
        context = f"Memory: {self.memory}\n\n" if self.memory else ""
        full_message = context + message
        
        response = self.chat.send_message(full_message)
        
        # Auto-store important info
        if "my name is" in message.lower():
            name = message.split("my name is")[-1].strip().split()[0]
            self.remember("user_name", name)
        
        return response.text

# Usage
agent = MemoryAgent()
agent.send_message("My name is Alice")
agent.send_message("What's my name?")  # Agent remembers
```

### Workflow Agent

```python
class WorkflowAgent:
    """Agent that executes multi-step workflows."""
    
    def __init__(self, workflow_steps):
        self.client = genai.Client()
        self.steps = workflow_steps
        self.results = []
    
    def execute_step(self, step, previous_result=None):
        """Execute a workflow step."""
        
        prompt = step['prompt']
        if previous_result:
            prompt = f"{prompt}\n\nPrevious result: {previous_result}"
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=step.get('tools', [])
            )
        )
        
        return response.text
    
    def run(self, initial_input):
        """Execute the workflow."""
        
        result = initial_input
        
        for i, step in enumerate(self.steps):
            print(f"Step {i+1}: {step['name']}")
            result = self.execute_step(step, result)
            self.results.append({
                'step': step['name'],
                'result': result
            })
        
        return result

# Usage
workflow = WorkflowAgent([
    {
        'name': 'Research',
        'prompt': 'Research this topic:',
        'tools': [types.Tool(google_search={})]
    },
    {
        'name': 'Analyze',
        'prompt': 'Analyze the research:'
    },
    {
        'name': 'Summarize',
        'prompt': 'Create a concise summary:'
    }
])

final_result = workflow.run("AI in education")
```

## Testing Your Agents

### Unit Tests

```python
import unittest
from google import genai

class TestSimpleAgent(unittest.TestCase):
    def setUp(self):
        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash"
        )
    
    def test_basic_response(self):
        response = self.chat.send_message("Hello")
        self.assertIsNotNone(response.text)
        self.assertGreater(len(response.text), 0)
    
    def test_context_retention(self):
        self.chat.send_message("My favorite color is blue")
        response = self.chat.send_message("What's my favorite color?")
        self.assertIn("blue", response.text.lower())

if __name__ == '__main__':
    unittest.main()
```

## Best Practices

1. **Start Simple** - Begin with basic agents and add complexity gradually
2. **Clear Instructions** - Use detailed system instructions
3. **Error Handling** - Always implement try-except blocks
4. **Testing** - Test agents with various inputs
5. **Logging** - Log interactions for debugging
6. **Resource Management** - Clean up files and close sessions
7. **Rate Limiting** - Implement backoff for API limits
8. **Security** - Validate inputs and sanitize outputs

## Troubleshooting

### Agent not responding correctly
- Check system instructions are clear
- Verify model choice is appropriate
- Review conversation history
- Test with simpler prompts

### Tool calls failing
- Verify function signatures match
- Check parameter types
- Ensure tools are properly declared
- Test tools independently

### Context lost in conversation
- Check history length limits
- Implement summarization
- Use system instructions for key context
- Consider stateful agent patterns

## Next Steps

- Review the [Workflows](../workflows/) guide for advanced patterns
- Check [Core Concepts](../core/) for deep dives
- Explore [Tools](../tools/) for more capabilities
- See [Setup](../setup/) for production configuration

## Contributing

Have a useful agent example? Please contribute! See [CONTRIBUTING.md](../../CONTRIBUTING.md).
