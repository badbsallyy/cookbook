# ReAct Pattern - Reasoning + Acting

## Overview

ReAct (Reasoning and Acting) is a powerful pattern that combines reasoning traces with action steps. It allows language models to generate thought processes while taking actions, making agent behavior more interpretable and effective.

## Core Concept

The ReAct pattern follows this loop:
1. **Thought**: Reason about what to do next
2. **Action**: Choose and execute a tool/action
3. **Observation**: Analyze the result
4. **Repeat** until task is complete

## Basic Implementation

### Simple ReAct Agent

```python
from google import genai
from google.genai import types

client = genai.Client()

# Define tools
def search(query: str) -> str:
    """Search for information."""
    # Simulate search
    return f"Search results for '{query}': [relevant information]"

def calculate(expression: str) -> float:
    """Calculate mathematical expression."""
    return eval(expression)

# ReAct system instruction
system_instruction = """You are a ReAct agent that follows this pattern:

Thought: Reason about what to do next
Action: Choose a tool to use (search or calculate)
Observation: Analyze the result
Repeat until you can provide the final answer.

Available actions:
- search(query): Search for information
- calculate(expression): Perform calculations
- finish(answer): Provide final answer

Format your response clearly showing Thought, Action, and Observation for each step.
"""

# Create agent
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [search, calculate],
        "system_instruction": system_instruction
    }
)

# Query
response = chat.send_message(
    "What is the population of Tokyo multiplied by 1.5?"
)
print(response.text)
```

## Structured ReAct Agent

### With Explicit Loop Control

```python
class ReActAgent:
    """Structured ReAct agent with explicit control."""
    
    def __init__(self, tools, max_iterations=5):
        self.client = genai.Client()
        self.tools = tools
        self.max_iterations = max_iterations
        self.history = []
    
    def think(self, user_query):
        """Generate thought about what to do."""
        
        system_instruction = """Generate your next thought about how to solve this task.
        Consider:
        - What information do you have?
        - What information do you need?
        - Which tool should you use next?
        
        Respond with just your thought, starting with "Thought:"
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Query: {user_query}\nHistory: {self.history}\n\nWhat's your next thought?",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        return response.text
    
    def act(self, thought):
        """Choose and execute an action."""
        
        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "tools": self.tools,
                "system_instruction": f"""Based on this thought: {thought}
                Choose the appropriate tool to use."""
            }
        )
        
        response = chat.send_message("Execute the appropriate action")
        return response.text
    
    def observe(self, action_result):
        """Analyze the observation."""
        
        system_instruction = """Analyze this observation.
        What did you learn?
        Can you answer the question now, or do you need more information?
        
        Respond with "Observation:" followed by your analysis.
        """
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Action result: {action_result}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        return response.text
    
    def should_continue(self, observation):
        """Decide if more iterations are needed."""
        
        if "finish" in observation.lower() or "answer is" in observation.lower():
            return False
        return True
    
    def run(self, query):
        """Run the ReAct loop."""
        
        print(f"Query: {query}\n")
        
        for iteration in range(self.max_iterations):
            print(f"--- Iteration {iteration + 1} ---")
            
            # Think
            thought = self.think(query)
            print(f"{thought}")
            self.history.append(f"Thought: {thought}")
            
            # Act
            action_result = self.act(thought)
            print(f"Action Result: {action_result}")
            self.history.append(f"Action: {action_result}")
            
            # Observe
            observation = self.observe(action_result)
            print(f"{observation}\n")
            self.history.append(observation)
            
            # Check if done
            if not self.should_continue(observation):
                break
        
        return "\n".join(self.history)

# Usage
def search(query: str) -> str:
    """Search for information."""
    return f"Results for {query}"

def calculate(expr: str) -> float:
    """Calculate expression."""
    return eval(expr)

agent = ReActAgent(tools=[search, calculate])
result = agent.run("What is 15 * 24?")
```

## Wikipedia Search Example

### Classic ReAct Implementation

```python
import wikipedia

def wikipedia_search(entity: str) -> str:
    """Search Wikipedia for an entity.
    
    Args:
        entity: Entity to search for
    """
    try:
        page = wikipedia.page(entity, auto_suggest=False)
        return page.content[:500]  # First 500 chars
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return f"Page not found for: {entity}"

def wikipedia_lookup(keyword: str) -> str:
    """Lookup keyword in current context."""
    # Simplified - in practice, maintain context
    return f"Found information about {keyword}"

system_instruction = """You are a ReAct agent that can search Wikipedia.

For each step:
Thought: Reason about what to do
Action: search(entity) or lookup(keyword)
Observation: Analyze what you found

Continue until you can answer the question.

Actions available:
- search(entity): Search Wikipedia
- lookup(keyword): Find keyword in context
- finish(answer): Provide final answer
"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [wikipedia_search, wikipedia_lookup],
        "system_instruction": system_instruction
    }
)

response = chat.send_message(
    "What is the elevation range of the High Plains in the United States?"
)
print(response.text)
```

## Advanced ReAct Patterns

### With Memory

```python
class ReActWithMemory:
    """ReAct agent with persistent memory."""
    
    def __init__(self, tools):
        self.client = genai.Client()
        self.tools = tools
        self.memory = []
        self.observations = []
    
    def add_to_memory(self, key, value):
        """Store information in memory."""
        self.memory.append({"key": key, "value": value})
    
    def recall(self, query):
        """Recall relevant information from memory."""
        # Simple keyword matching
        relevant = [m for m in self.memory if query.lower() in str(m).lower()]
        return relevant
    
    def run(self, query):
        """Run with memory integration."""
        
        # Check memory first
        recalled = self.recall(query)
        memory_context = "\n".join([str(m) for m in recalled])
        
        system_instruction = f"""You are a ReAct agent with memory.

Memory: {memory_context}

Use ReAct pattern (Thought-Action-Observation) to solve tasks.
Store important information in memory for future use.
"""
        
        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "tools": self.tools,
                "system_instruction": system_instruction
            }
        )
        
        response = chat.send_message(query)
        
        # Extract and store important information
        # (simplified - would use more sophisticated extraction)
        if "answer" in response.text.lower():
            self.add_to_memory(query, response.text)
        
        return response.text

# Usage
agent = ReActWithMemory(tools=[search, calculate])
result1 = agent.run("What is 10 * 20?")
result2 = agent.run("What was my previous calculation?")
```

### Multi-Tool ReAct

```python
def web_search(query: str) -> str:
    """Search the web."""
    return f"Web results for: {query}"

def database_query(sql: str) -> str:
    """Query database."""
    return f"Query results: {sql}"

def file_read(path: str) -> str:
    """Read file."""
    return f"File contents of {path}"

def send_email(to: str, subject: str, body: str) -> str:
    """Send email."""
    return f"Email sent to {to}"

system_instruction = """You are a multi-tool ReAct agent.

Available tools:
- web_search(query): Search the internet
- database_query(sql): Query database
- file_read(path): Read files
- send_email(to, subject, body): Send emails

Use ReAct pattern to complete complex tasks involving multiple tools.

Format:
Thought: [reasoning]
Action: [tool(args)]
Observation: [result analysis]
"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [web_search, database_query, file_read, send_email],
        "system_instruction": system_instruction
    }
)

response = chat.send_message("""
Find the latest sales data from the database,
read the report template file,
and send a summary email to the manager.
""")
```

## Error Recovery

### ReAct with Error Handling

```python
class RobustReActAgent:
    """ReAct agent with error recovery."""
    
    def __init__(self, tools, max_retries=3):
        self.client = genai.Client()
        self.tools = tools
        self.max_retries = max_retries
        self.error_count = 0
    
    def run(self, query):
        """Run with error recovery."""
        
        system_instruction = """You are a ReAct agent with error recovery.

If an action fails:
1. Analyze why it failed
2. Try an alternative approach
3. If stuck, ask for clarification

Use Thought-Action-Observation pattern.
"""
        
        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "tools": self.tools,
                "system_instruction": system_instruction
            }
        )
        
        for attempt in range(self.max_retries):
            try:
                response = chat.send_message(query)
                self.error_count = 0
                return response.text
                
            except Exception as e:
                self.error_count += 1
                
                if self.error_count >= self.max_retries:
                    return f"Failed after {self.max_retries} attempts: {e}"
                
                # Inform agent of error
                error_msg = f"Previous attempt failed: {e}. Try a different approach."
                query = f"{query}\n\nError: {error_msg}"
        
        return "Max retries exceeded"
```

## Best Practices

1. **Clear thought articulation**: Make reasoning explicit
2. **Structured output**: Use consistent format for thoughts/actions/observations
3. **Tool selection strategy**: Choose appropriate tools for each step
4. **Iteration limits**: Prevent infinite loops
5. **Error handling**: Handle tool failures gracefully
6. **Memory integration**: Store and recall important information
7. **Observation analysis**: Extract useful information from results
8. **Early termination**: Stop when answer is found

## Complete Example

```python
class ProductionReActAgent:
    """Production-ready ReAct agent."""
    
    def __init__(self, tools, max_iterations=10):
        self.client = genai.Client()
        self.tools = tools
        self.max_iterations = max_iterations
        self.trace = []
    
    def run(self, query):
        """Execute ReAct pattern."""
        
        system_instruction = """You are a ReAct agent that solves problems step by step.

For each step:
1. Thought: Explain your reasoning
2. Action: Choose a tool to use
3. Observation: Analyze the result

Continue until you can provide a definitive answer.

Format your response as:
Thought: [your reasoning]
Action: [tool to use]
Observation: [analysis]

When ready, use finish(answer) to complete the task.
"""
        
        chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "tools": self.tools,
                "system_instruction": system_instruction,
                "temperature": 0.4
            }
        )
        
        print(f"Query: {query}\n")
        
        for i in range(self.max_iterations):
            try:
                response = chat.send_message(
                    query if i == 0 else "Continue with next step"
                )
                
                text = response.text
                print(f"Step {i+1}:")
                print(text)
                print()
                
                self.trace.append({
                    "step": i+1,
                    "response": text
                })
                
                # Check if finished
                if "finish(" in text.lower() or "final answer" in text.lower():
                    break
                    
            except Exception as e:
                print(f"Error at step {i+1}: {e}")
                break
        
        return {
            "final_response": text,
            "trace": self.trace,
            "steps": len(self.trace)
        }

# Usage
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"

def calculate(expr: str) -> str:
    """Calculate expression."""
    try:
        result = eval(expr)
        return str(result)
    except:
        return "Calculation error"

agent = ProductionReActAgent(tools=[search, calculate])
result = agent.run("What is the square root of 144 plus 10?")

print("\n--- Summary ---")
print(f"Completed in {result['steps']} steps")
print(f"Final Answer: {result['final_response']}")
```

## Next Steps

- [Prompt Chaining](chaining.md) - Chain multiple prompts
- [Multi-Turn Conversations](multi-turn.md) - Build conversational agents
- [Function Calling](../tools/function-calling.md) - Add more tools
