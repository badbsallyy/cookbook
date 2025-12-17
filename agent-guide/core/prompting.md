# Prompting Guide

## Overview

Effective prompting is crucial for building successful AI agents. This guide covers system instructions, prompt engineering techniques, and best practices for the Gemini API.

## System Instructions

System instructions allow you to set persistent behavior for the model throughout a conversation.

### Basic Usage

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How should I approach this problem?",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful problem-solving assistant. Break down complex problems into clear steps."
    )
)

print(response.text)
```

### System Instruction Examples

#### Agent Assistant

```python
system_instruction = """You are an AI agent assistant that:
- Breaks down complex tasks into actionable steps
- Uses available tools when appropriate
- Explains your reasoning process
- Asks clarifying questions when needed
- Provides concise, practical responses
"""
```

#### Code Assistant

```python
system_instruction = """You are an expert programming assistant that:
- Writes clean, well-documented code
- Follows best practices and design patterns
- Explains code logic clearly
- Suggests optimizations when relevant
- Uses type hints and proper error handling
"""
```

#### Data Analyst

```python
system_instruction = """You are a data analysis expert that:
- Analyzes data systematically
- Identifies patterns and insights
- Presents findings clearly with visualizations
- Recommends actionable next steps
- Validates assumptions with data
"""
```

## Prompt Engineering Techniques

### 1. Be Specific and Clear

❌ **Vague:**
```
Tell me about Python
```

✅ **Specific:**
```
Explain how to use list comprehensions in Python with 3 practical examples
```

### 2. Provide Context

```python
prompt = """Context: I'm building a web scraping agent that needs to extract product information from e-commerce sites.

Task: Write a Python function that:
1. Takes a URL as input
2. Extracts product name, price, and description
3. Returns a structured dictionary
4. Handles errors gracefully

Requirements:
- Use BeautifulSoup4
- Include error handling for network issues
- Add type hints
"""
```

### 3. Use Step-by-Step Instructions

```python
prompt = """Analyze this error and help me fix it:

Error: TypeError: 'NoneType' object is not subscriptable

Steps to follow:
1. Explain what this error means
2. Identify likely causes
3. Provide 2-3 specific solutions
4. Show code examples for each solution
"""
```

### 4. Specify Output Format

```python
prompt = """Analyze this customer feedback and structure your response as:

Sentiment: [Positive/Negative/Neutral]
Key Issues: [Bullet list]
Priority: [High/Medium/Low]
Recommended Action: [Brief description]

Feedback: "The product quality is great but delivery was very slow"
"""
```

### 5. Use Examples (Few-Shot Learning)

```python
prompt = """Extract structured information from text. Follow these examples:

Example 1:
Input: "John Smith, age 30, lives in New York"
Output: {"name": "John Smith", "age": 30, "city": "New York"}

Example 2:
Input: "Sarah Johnson, 25 years old, from London"
Output: {"name": "Sarah Johnson", "age": 25, "city": "London"}

Now extract from:
Input: "Mike Davis, aged 35, resident of Tokyo"
Output:
"""
```

### 6. Chain of Thought Prompting

```python
prompt = """Let's solve this step by step:

Problem: A store sells 3 types of items. Type A costs $10, Type B costs $15, and Type C costs $25. If someone buys 2 of Type A, 3 of Type B, and 1 of Type C, what's the total cost?

Please show your reasoning:
1. Calculate cost for each type
2. Sum the totals
3. Provide the final answer
"""
```

## Agent-Specific Prompting

### ReAct Pattern Prompt

```python
system_instruction = """You are an agent that follows the ReAct (Reasoning + Acting) pattern:

For each step:
1. Thought: Reason about what to do next
2. Action: Choose a tool to use
3. Observation: Analyze the result
4. Repeat until task is complete

Available tools:
- search(query): Search for information
- calculate(expression): Perform calculations
- get_date(): Get current date

Format your response as:
Thought: [Your reasoning]
Action: [tool_name(arguments)]
Observation: [Result analysis]
"""
```

### Multi-Turn Conversation

```python
# First turn - establish context
messages = [
    {
        "role": "user",
        "parts": [{"text": "I'm building a chatbot. Help me design it."}]
    }
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages
)

# Second turn - follow up
messages.append({
    "role": "model",
    "parts": [{"text": response.text}]
})

messages.append({
    "role": "user",
    "parts": [{"text": "What libraries should I use for the backend?"}]
})

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages
)
```

## Best Practices

### 1. Temperature Control

```python
# For factual, deterministic responses (agents, code)
config = {"temperature": 0.2}

# For balanced responses
config = {"temperature": 0.7}

# For creative responses
config = {"temperature": 1.2}
```

### 2. Token Management

```python
# Limit response length
config = {
    "max_output_tokens": 1024,
    "stop_sequences": ["END", "###"]
}
```

### 3. Error Recovery

```python
prompt = """If you don't know something or are uncertain:
1. Clearly state what you don't know
2. Explain what information you'd need
3. Suggest alternatives or next steps

Don't make up information or guess.
"""
```

### 4. Structured Outputs

Request specific formats:

```python
prompt = """Analyze this code and respond in JSON format:
{
    "bugs": ["list of issues"],
    "suggestions": ["list of improvements"],
    "complexity": "low|medium|high"
}

Code:
[your code here]
"""
```

## Common Pitfalls to Avoid

1. ❌ **Too vague**: "Help me with my code"
2. ❌ **No context**: "Fix this bug" (without showing code)
3. ❌ **Conflicting instructions**: "Be brief but explain everything in detail"
4. ❌ **Assuming knowledge**: Not explaining domain-specific terms
5. ❌ **No examples**: Not showing desired output format

## Advanced Techniques

### Prompt Chaining

Break complex tasks into steps:

```python
# Step 1: Generate outline
outline_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Create an outline for a blog post about AI agents"
)

# Step 2: Expand each section
section_prompt = f"Expand this section: {outline_response.text.split('\n')[0]}"
section_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=section_prompt
)
```

### Self-Correction

```python
system_instruction = """After providing an answer:
1. Review your response for accuracy
2. Identify potential issues or gaps
3. Provide corrections if needed

Format:
Answer: [Your response]
Self-Review: [Check for issues]
Corrections: [If any]
"""
```

### Meta-Prompting

```python
prompt = """You are an expert prompt engineer. Improve this prompt:

Original: "Write a function"

Requirements:
- Make it specific
- Add context
- Specify output format
- Include examples

Improved Prompt:
"""
```

## Testing Your Prompts

1. **Test with edge cases**: Unusual inputs, empty values
2. **Verify consistency**: Run same prompt multiple times
3. **Check different models**: Test with various Gemini models
4. **Measure quality**: Evaluate responses against criteria
5. **Iterate**: Refine based on results

## Examples

### Complete Agent Prompt

```python
from google import genai
from google.genai import types

client = genai.Client()

system_instruction = """You are a research assistant agent.

Your capabilities:
- Search for information using available tools
- Synthesize information from multiple sources
- Cite sources for factual claims
- Admit when you don't know something

Your response format:
1. Understanding: Restate the question
2. Research: What information you need
3. Analysis: Key findings
4. Conclusion: Direct answer with sources
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the latest developments in quantum computing?",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.4
    )
)

print(response.text)
```

## Next Steps

- [Streaming Responses](streaming.md) - Handle real-time streaming
- [JSON Mode](json-mode.md) - Get structured outputs
- [Function Calling](../tools/function-calling.md) - Add tools to agents
- [ReAct Pattern](../workflows/react-pattern.md) - Implement reasoning agents
