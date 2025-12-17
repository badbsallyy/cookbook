# Gemini Models Overview

## Overview

The Gemini API offers various models optimized for different use cases. This guide helps you choose the right model for your agent.

## Available Models

### Gemini 2.5 Flash (Recommended for Agents)

**Model ID:** `gemini-2.5-flash`

- **Best for:** General-purpose agents, function calling, most production use cases
- **Context Window:** 1M tokens
- **Speed:** Fast
- **Cost:** Low
- **Capabilities:** Text, images, audio, video, function calling, code execution

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI agents work"
)
```

### Gemini 2.5 Flash Lite

**Model ID:** `gemini-2.5-flash-lite`

- **Best for:** High-volume, simple queries, cost-sensitive applications
- **Context Window:** 1M tokens
- **Speed:** Fastest
- **Cost:** Lowest
- **Capabilities:** Text, basic reasoning

### Gemini 2.5 Pro

**Model ID:** `gemini-2.5-pro`

- **Best for:** Complex reasoning, advanced problem solving, detailed analysis
- **Context Window:** 2M tokens
- **Speed:** Moderate
- **Cost:** Higher
- **Capabilities:** Advanced reasoning, complex task decomposition

```python
# Use for complex reasoning tasks
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Design a complete architecture for a distributed system with detailed tradeoffs"
)
```

### Gemini 3 Pro Preview

**Model ID:** `gemini-3-pro-preview`

- **Best for:** Experimental features, cutting-edge capabilities
- **Context Window:** Variable
- **Speed:** Variable
- **Cost:** Higher
- **Note:** Preview model, may have breaking changes

## Listing Available Models

### Get All Models

```python
from google import genai

client = genai.Client()

# List all available models
for model in client.models.list():
    print(f"{model.name}")
```

### Filter by Capability

```python
# Find models that support generateContent
text_models = []
for model in client.models.list():
    if "generateContent" in model.supported_actions:
        text_models.append(model.name)

print("Text generation models:", text_models)

# Find embedding models
embedding_models = []
for model in client.models.list():
    if "embedContent" in model.supported_actions:
        embedding_models.append(model.name)

print("Embedding models:", embedding_models)
```

## Model Details

### Get Model Information

```python
def get_model_info(model_name):
    """Get detailed information about a model"""
    
    for model in client.models.list():
        if model.name == f"models/{model_name}":
            print(f"Name: {model.display_name}")
            print(f"Description: {model.description}")
            print(f"Input Token Limit: {model.input_token_limit:,}")
            print(f"Output Token Limit: {model.output_token_limit:,}")
            print(f"Supported Actions: {', '.join(model.supported_actions)}")
            return model
    
    return None

# Usage
model_info = get_model_info("gemini-2.5-flash")
```

### Example Output

```
Name: Gemini 2.5 Flash
Description: Mid-size multimodal model supporting up to 1M tokens
Input Token Limit: 1,048,576
Output Token Limit: 65,536
Supported Actions: generateContent, countTokens, createCachedContent
```

## Model Selection Guide

### Choose Based on Task

| Task Type | Recommended Model | Reason |
|-----------|------------------|---------|
| Simple Q&A | gemini-2.5-flash-lite | Fast, cost-effective |
| Agent with tools | gemini-2.5-flash | Balanced performance |
| Complex reasoning | gemini-2.5-pro | Best reasoning capability |
| High-volume processing | gemini-2.5-flash-lite | Lowest cost |
| Multimodal tasks | gemini-2.5-flash | Good multimodal support |
| Code generation | gemini-2.5-flash | Strong code capabilities |

### Choose Based on Context Size

```python
def recommend_model_by_context(input_tokens):
    """Recommend model based on input size"""
    
    if input_tokens < 100_000:
        return "gemini-2.5-flash-lite"
    elif input_tokens < 1_000_000:
        return "gemini-2.5-flash"
    else:
        return "gemini-2.5-pro"

# Usage
recommended = recommend_model_by_context(500_000)
print(f"Recommended: {recommended}")
```

## Model Comparison

### Performance vs Cost

```
High Performance  ←→  Low Cost
───────────────────────────────
gemini-2.5-pro
gemini-2.5-flash
gemini-2.5-flash-lite
```

### Speed vs Capability

```
High Speed  ←→  High Capability
───────────────────────────────
gemini-2.5-flash-lite
gemini-2.5-flash
gemini-2.5-pro
```

## Agent-Specific Considerations

### For ReAct Agents

Use `gemini-2.5-flash` for good balance of:
- Reasoning capability
- Tool use
- Speed
- Cost

```python
system_instruction = """You are a ReAct agent.
Follow Thought-Action-Observation pattern."""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Find and analyze recent AI developments",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[...]  # Your tools
    )
)
```

### For Conversational Agents

Use `gemini-2.5-flash` for:
- Multi-turn conversations
- Context retention
- Natural responses

```python
# Maintain conversation history
messages = []

# Use same model throughout conversation
model = "gemini-2.5-flash"

for turn in conversation:
    messages.append({"role": "user", "parts": [{"text": turn}]})
    response = client.models.generate_content(
        model=model,
        contents=messages
    )
    messages.append({"role": "model", "parts": [{"text": response.text}]})
```

### For Data Processing Agents

Use `gemini-2.5-flash-lite` for:
- High-volume processing
- Simple extraction
- Classification tasks

```python
# Process large batch of items
results = []
for item in large_dataset:
    result = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"Classify: {item}"
    )
    results.append(result.text)
```

## Model Fallback Strategy

### Implement Graceful Degradation

```python
class ModelFallback:
    """Try models in order of preference"""
    
    def __init__(self, client):
        self.client = client
        self.models = [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite"
        ]
    
    def generate(self, prompt):
        """Try models until one succeeds"""
        
        for model in self.models:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text, model
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue
        
        raise Exception("All models failed")

# Usage
fallback = ModelFallback(client)
result, used_model = fallback.generate("Your prompt")
print(f"Used model: {used_model}")
```

## Cost Optimization

### Strategy for Cost Reduction

```python
def choose_model_by_complexity(prompt):
    """Choose cheapest model that can handle task"""
    
    # Simple heuristics
    word_count = len(prompt.split())
    has_code = "```" in prompt or "def " in prompt
    needs_reasoning = any(word in prompt.lower() 
                         for word in ["analyze", "compare", "evaluate"])
    
    if needs_reasoning or has_code:
        return "gemini-2.5-flash"
    elif word_count > 1000:
        return "gemini-2.5-flash"
    else:
        return "gemini-2.5-flash-lite"

# Usage
model = choose_model_by_complexity(user_prompt)
response = client.models.generate_content(
    model=model,
    contents=user_prompt
)
```

## Token Counting

### Check Token Usage

```python
def count_tokens(text, model="gemini-2.5-flash"):
    """Count tokens in text"""
    
    result = client.models.count_tokens(
        model=model,
        contents=text
    )
    
    return result.total_tokens

# Usage
prompt = "Your long prompt here..."
tokens = count_tokens(prompt)
print(f"Token count: {tokens}")

# Check if within limits
model_info = get_model_info("gemini-2.5-flash")
if tokens > model_info.input_token_limit:
    print("Prompt too long!")
```

## Best Practices

1. **Start with gemini-2.5-flash** - Good default for most agents
2. **Use flash-lite for simple tasks** - Reduce costs on high-volume operations
3. **Reserve pro for complex reasoning** - Only when flash isn't sufficient
4. **Test with different models** - Measure quality vs cost tradeoffs
5. **Implement fallbacks** - Handle model unavailability
6. **Monitor token usage** - Stay within limits
7. **Cache when possible** - Reuse common contexts
8. **Consider batch processing** - For high-volume operations

## Model Updates

### Stay Current

```python
def check_for_new_models():
    """Check for newly available models"""
    
    known_models = ["gemini-2.5-flash", "gemini-2.5-pro"]
    current_models = [m.name for m in client.models.list()]
    
    new_models = [m for m in current_models 
                  if m not in known_models and "preview" not in m]
    
    if new_models:
        print("New models available:")
        for model in new_models:
            print(f"  - {model}")

# Run periodically
check_for_new_models()
```

## Next Steps

- [Prompting Guide](prompting.md) - Optimize prompts for each model
- [Function Calling](../tools/function-calling.md) - Add tools to models
- [Streaming](streaming.md) - Stream responses
- [Error Handling](error-handling.md) - Handle model errors
