# Multi-Turn Conversations

## Overview

Multi-turn conversations enable agents to maintain context across multiple interactions, creating natural dialogues and stateful agents that remember previous exchanges.

## Basic Multi-Turn

### Simple Conversation

```python
from google import genai
from google.genai import types

client = genai.Client()

# Start chat session
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "system_instruction": "You are a helpful assistant"
    }
)

# First turn
response1 = chat.send_message("Hello! My name is Alice.")
print(f"User: Hello! My name is Alice.")
print(f"Agent: {response1.text}\n")

# Second turn - agent remembers name
response2 = chat.send_message("What's my name?")
print(f"User: What's my name?")
print(f"Agent: {response2.text}\n")

# Third turn - build on context
response3 = chat.send_message("Can you help me with Python?")
print(f"User: Can you help me with Python?")
print(f"Agent: {response3.text}")
```

## Chat History

### Access Conversation History

```python
# Create chat
chat = client.chats.create(model="gemini-2.5-flash")

# Multiple turns
chat.send_message("I need help with machine learning")
chat.send_message("Specifically, I want to learn about neural networks")
chat.send_message("What are the basic components?")

# Get history
history = chat.get_history()

print("Conversation History:")
for i, content in enumerate(history):
    role = content.role
    text = content.parts[0].text if content.parts else ""
    print(f"{i+1}. {role}: {text[:100]}...")
```

### Manual History Management

```python
messages = []

def send_with_history(user_message):
    """Send message with explicit history management."""
    
    # Add user message
    messages.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })
    
    # Generate response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
    )
    
    # Add model response
    messages.append({
        "role": "model",
        "parts": [{"text": response.text}]
    })
    
    return response.text

# Usage
response1 = send_with_history("Hello")
response2 = send_with_history("Tell me about AI")
response3 = send_with_history("Can you give me an example?")
```

## Stateful Agents

### Agent with Memory

```python
class StatefulAgent:
    """Agent that maintains state across conversations."""
    
    def __init__(self, name="Assistant"):
        self.client = genai.Client()
        self.name = name
        self.user_info = {}
        self.conversation_context = []
        self.chat = None
    
    def start_conversation(self):
        """Initialize a new conversation."""
        
        system_instruction = f"""You are {self.name}, a helpful assistant.
        Maintain context throughout the conversation.
        Remember user preferences and information.
        """
        
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": system_instruction}
        )
    
    def remember(self, key, value):
        """Store user information."""
        self.user_info[key] = value
    
    def recall(self, key):
        """Retrieve user information."""
        return self.user_info.get(key)
    
    def send_message(self, message):
        """Send message with context awareness."""
        
        if not self.chat:
            self.start_conversation()
        
        # Extract and store important information
        if "my name is" in message.lower():
            name = message.split("my name is")[-1].strip().split()[0]
            self.remember("name", name)
        
        # Add context to message if relevant
        context = ""
        if self.user_info:
            context = f"\n[User info: {self.user_info}]"
        
        response = self.chat.send_message(message + context)
        
        self.conversation_context.append({
            "user": message,
            "agent": response.text
        })
        
        return response.text
    
    def get_summary(self):
        """Summarize the conversation."""
        
        history_text = "\n".join([
            f"User: {turn['user']}\nAgent: {turn['agent']}"
            for turn in self.conversation_context
        ])
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize this conversation:\n{history_text}"
        )
        
        return response.text

# Usage
agent = StatefulAgent(name="Alex")
agent.start_conversation()

agent.send_message("Hi! My name is John.")
agent.send_message("I'm interested in learning Python.")
agent.send_message("What should I start with?")

print(agent.get_summary())
```

## Context Management

### Sliding Window Context

```python
class SlidingWindowChat:
    """Chat with limited context window."""
    
    def __init__(self, max_turns=10):
        self.client = genai.Client()
        self.messages = []
        self.max_turns = max_turns
    
    def add_message(self, role, content):
        """Add message to history."""
        self.messages.append({
            "role": role,
            "parts": [{"text": content}]
        })
        
        # Keep only last N turns (2 messages per turn)
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-(self.max_turns * 2):]
    
    def send_message(self, user_message):
        """Send message with sliding window."""
        
        self.add_message("user", user_message)
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=self.messages
        )
        
        self.add_message("model", response.text)
        
        return response.text

# Usage
chat = SlidingWindowChat(max_turns=5)
for i in range(10):
    response = chat.send_message(f"Message {i+1}")
```

### Conversation Summarization

```python
class SummarizedChat:
    """Chat that summarizes old context."""
    
    def __init__(self, summarize_after=5):
        self.client = genai.Client()
        self.messages = []
        self.summary = ""
        self.summarize_after = summarize_after
        self.turn_count = 0
    
    def summarize_history(self):
        """Create summary of conversation history."""
        
        history_text = "\n".join([
            f"{msg['role']}: {msg['parts'][0]['text']}"
            for msg in self.messages
        ])
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize this conversation concisely:\n{history_text}"
        )
        
        self.summary = response.text
        self.messages = []  # Clear old messages
    
    def send_message(self, user_message):
        """Send message with periodic summarization."""
        
        self.turn_count += 1
        
        # Summarize if needed
        if self.turn_count % self.summarize_after == 0:
            self.summarize_history()
        
        # Create context with summary
        context = []
        if self.summary:
            context.append({
                "role": "user",
                "parts": [{"text": f"[Previous context: {self.summary}]"}]
            })
        
        context.extend(self.messages)
        context.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=context
        )
        
        # Add to history
        self.messages.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })
        self.messages.append({
            "role": "model",
            "parts": [{"text": response.text}]
        })
        
        return response.text
```

## Interactive Loops

### Command-Line Chat

```python
def interactive_chat():
    """Run interactive chat session."""
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": "You are a helpful AI assistant"
        }
    )
    
    print("Chat started. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Agent: Goodbye!")
            break
        
        if not user_input.strip():
            continue
        
        response = chat.send_message(user_input)
        print(f"Agent: {response.text}\n")

# Usage
interactive_chat()
```

### With Tool Integration

```python
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"

def calculate(expression: str) -> float:
    """Calculate expression."""
    return eval(expression)

def interactive_agent():
    """Interactive agent with tools."""
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "tools": [search, calculate],
            "system_instruction": """You are an AI assistant with access to:
            - search: Find information
            - calculate: Do math
            
            Use these tools to help the user."""
        }
    )
    
    print("Multi-tool agent ready. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            break
        
        response = chat.send_message(user_input)
        print(f"Agent: {response.text}\n")

# Usage
interactive_agent()
```

## Conversation Flows

### Guided Conversation

```python
class GuidedConversation:
    """Agent that guides user through structured flow."""
    
    def __init__(self, flow_steps):
        self.client = genai.Client()
        self.flow_steps = flow_steps
        self.current_step = 0
        self.collected_info = {}
        self.chat = None
    
    def start(self):
        """Start the guided conversation."""
        
        system_instruction = f"""You are guiding a user through this process:
        {', '.join(self.flow_steps)}
        
        Ask one question at a time and collect the information."""
        
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": system_instruction}
        )
        
        # Ask first question
        return self.next_step()
    
    def next_step(self):
        """Move to next step in flow."""
        
        if self.current_step >= len(self.flow_steps):
            return "All information collected!"
        
        step = self.flow_steps[self.current_step]
        response = self.chat.send_message(
            f"Ask the user about: {step}"
        )
        
        return response.text
    
    def process_response(self, user_response):
        """Process user response and move to next step."""
        
        # Store response
        step_name = self.flow_steps[self.current_step]
        self.collected_info[step_name] = user_response
        
        # Move to next step
        self.current_step += 1
        
        if self.current_step < len(self.flow_steps):
            return self.next_step()
        else:
            return self.summarize()
    
    def summarize(self):
        """Summarize collected information."""
        
        summary_prompt = f"Summarize this information:\n{self.collected_info}"
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=summary_prompt
        )
        
        return response.text

# Usage
flow = GuidedConversation([
    "name",
    "email",
    "preferred programming language",
    "project goals"
])

print(flow.start())
# Then call flow.process_response(user_input) for each response
```

## Advanced Patterns

### Multi-Session Agent

```python
class MultiSessionAgent:
    """Agent that maintains multiple conversation sessions."""
    
    def __init__(self):
        self.client = genai.Client()
        self.sessions = {}
    
    def create_session(self, session_id, context=None):
        """Create a new conversation session."""
        
        system_instruction = f"You are a helpful assistant."
        if context:
            system_instruction += f"\nContext: {context}"
        
        self.sessions[session_id] = self.client.chats.create(
            model="gemini-2.5-flash",
            config={"system_instruction": system_instruction}
        )
    
    def send_message(self, session_id, message):
        """Send message to specific session."""
        
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        return self.sessions[session_id].send_message(message).text
    
    def get_session_summary(self, session_id):
        """Get summary of a session."""
        
        if session_id not in self.sessions:
            return "Session not found"
        
        history = self.sessions[session_id].get_history()
        history_text = "\n".join([
            f"{content.role}: {content.parts[0].text if content.parts else ''}"
            for content in history
        ])
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize this conversation:\n{history_text}"
        )
        
        return response.text

# Usage
agent = MultiSessionAgent()

# Different conversations
agent.send_message("user1", "Help me with Python")
agent.send_message("user2", "Tell me about JavaScript")
agent.send_message("user1", "Show me a for loop example")
```

## Best Practices

1. **Maintain context**: Use chat sessions for related interactions
2. **Manage history length**: Implement sliding windows or summarization
3. **Clear system instructions**: Set conversation guidelines
4. **Handle interruptions**: Support conversation resumption
5. **Extract information**: Store important details from conversation
6. **Provide summaries**: Offer conversation recaps
7. **Implement timeouts**: Handle inactive conversations
8. **Test conversation flows**: Verify multi-turn interactions

## Complete Example

```python
class ProductionChatAgent:
    """Production-ready multi-turn chat agent."""
    
    def __init__(self, name="Assistant", max_history=20):
        self.client = genai.Client()
        self.name = name
        self.max_history = max_history
        self.chat = None
        self.start_time = None
        self.user_info = {}
    
    def start(self):
        """Start conversation."""
        
        from datetime import datetime
        self.start_time = datetime.now()
        
        system_instruction = f"""You are {self.name}, a helpful AI assistant.
        - Maintain context throughout conversation
        - Be friendly and professional
        - Ask clarifying questions when needed
        - Provide accurate, helpful information
        """
        
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "system_instruction": system_instruction,
                "temperature": 0.7
            }
        )
    
    def send_message(self, message):
        """Send message with full error handling."""
        
        if not self.chat:
            self.start()
        
        try:
            response = self.chat.send_message(message)
            
            # Trim history if too long
            history = self.chat.get_history()
            if len(history) > self.max_history:
                # Would need to create new chat with summary
                pass
            
            return response.text
            
        except Exception as e:
            return f"Error: {e}"
    
    def get_summary(self):
        """Get conversation summary."""
        
        history = self.chat.get_history()
        history_text = "\n".join([
            f"{content.role}: {content.parts[0].text if content.parts else ''}"[:200]
            for content in history
        ])
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Provide a brief summary of this conversation:\n{history_text}"
        )
        
        return response.text

# Usage
agent = ProductionChatAgent(name="Alex")
agent.start()

# Conversation
print(agent.send_message("Hello!"))
print(agent.send_message("I need help with Python"))
print(agent.send_message("Can you show me an example?"))

# Get summary
print("\nSummary:", agent.get_summary())
```

## Next Steps

- [ReAct Pattern](react-pattern.md) - Add reasoning to conversations
- [Chaining](chaining.md) - Chain conversation steps
- [Function Calling](../tools/function-calling.md) - Add tools to conversations
