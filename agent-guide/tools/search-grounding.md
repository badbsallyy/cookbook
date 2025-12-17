# Search & Grounding

## Overview

Grounding connects Gemini models to real-time information from Google Search and other sources. This is essential for agents that need current information, facts, and web data.

## Google Search Grounding

### Basic Search

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the latest developments in AI?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search={})]
    )
)

print(response.text)
```

### With Dynamic Retrieval

```python
# Dynamic retrieval automatically decides when to search
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the current weather in Tokyo?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search={})],
        response_modalities=["TEXT"]
    )
)

print(response.text)
```

## Grounding Metadata

### Access Search Queries

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the latest news about quantum computing?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search={})]
    )
)

# Access grounding metadata
if hasattr(response, 'grounding_metadata'):
    metadata = response.grounding_metadata
    
    # Search queries used
    if hasattr(metadata, 'search_entry_point'):
        print("Search queries:")
        for query in metadata.search_entry_point.rendered_content:
            print(f"  - {query}")
    
    # Grounding chunks
    if hasattr(metadata, 'grounding_chunks'):
        print("\nSources:")
        for chunk in metadata.grounding_chunks:
            if hasattr(chunk, 'web'):
                print(f"  - {chunk.web.title}: {chunk.web.uri}")

print(f"\nResponse: {response.text}")
```

## Agent Integration

### Research Agent

```python
system_instruction = """You are a research agent.
Use Google Search to find current information.
Always cite your sources."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(google_search={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message(
    "What are the top 3 trends in artificial intelligence in 2025?"
)
print(response.text)
```

### Fact-Checking Agent

```python
system_instruction = """You are a fact-checking agent.
For each claim:
1. Search for reliable sources
2. Verify the information
3. Cite your sources
4. Provide a verdict (True/False/Uncertain)"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(google_search={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message(
    "Is it true that Python 3.13 was released in 2024?"
)
print(response.text)
```

### News Summarization Agent

```python
system_instruction = """You are a news summarization agent.
Search for recent news on the given topic and provide:
1. Brief summary of each major story
2. Key developments
3. Sources
"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(google_search={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message(
    "Summarize recent news about SpaceX launches"
)
print(response.text)
```

## Combining with Other Tools

### Search + Function Calling

```python
def save_research(topic: str, content: str) -> str:
    """Save research results.
    
    Args:
        topic: Research topic
        content: Research content
    """
    # Save to database or file
    return f"Saved research on '{topic}'"

# Combine search with function calling
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [
            types.Tool(google_search={}),
            save_research
        ],
        "system_instruction": "Research topics and save the results"
    }
)

response = chat.send_message(
    "Research the latest AI breakthroughs and save them"
)
print(response.text)
```

### Search + Code Execution

```python
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [
            types.Tool(google_search={}),
            types.Tool(code_execution={})
        ],
        "system_instruction": "Research data and analyze it with code"
    }
)

response = chat.send_message("""
Find the GDP growth rates for top 5 economies in 2024,
then calculate the average growth rate.
""")
print(response.text)
```

## Advanced Patterns

### Multi-Query Research

```python
def research_topic(topic, num_queries=3):
    """Research a topic with multiple queries."""
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "tools": [types.Tool(google_search={})],
            "system_instruction": """Break down the topic into sub-questions
            and research each one."""
        }
    )
    
    response = chat.send_message(f"""
    Research this topic thoroughly: {topic}
    
    Generate {num_queries} different search queries to cover all aspects,
    then synthesize the findings.
    """)
    
    return response.text

# Usage
result = research_topic("Impact of AI on healthcare", num_queries=3)
print(result)
```

### Iterative Research

```python
def iterative_research(initial_query, depth=3):
    """Perform iterative research, going deeper each time."""
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "tools": [types.Tool(google_search={})],
            "system_instruction": "Research topics deeply, following interesting leads"
        }
    )
    
    # Initial research
    response = chat.send_message(initial_query)
    print(f"Initial findings:\n{response.text}\n")
    
    # Follow-up questions
    for i in range(depth):
        follow_up = chat.send_message(
            "Based on that, what are the most interesting findings that need deeper investigation?"
        )
        print(f"Depth {i+1}:\n{follow_up.text}\n")

# Usage
iterative_research("What is quantum computing?", depth=2)
```

## Grounding Configuration

### Control Search Behavior

```python
# More precise grounding
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Latest iPhone features",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search={})],
        grounding_config={
            "threshold": 0.8,  # Higher threshold for more confident grounding
        }
    )
)
```

## Citation Management

### Extract Citations

```python
def extract_citations(response):
    """Extract and format citations from response."""
    
    citations = []
    
    if hasattr(response, 'grounding_metadata'):
        metadata = response.grounding_metadata
        
        if hasattr(metadata, 'grounding_chunks'):
            for chunk in metadata.grounding_chunks:
                if hasattr(chunk, 'web'):
                    citations.append({
                        'title': chunk.web.title,
                        'url': chunk.web.uri
                    })
    
    return citations

# Usage
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="History of artificial intelligence",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search={})]
    )
)

citations = extract_citations(response)
print("Sources:")
for i, citation in enumerate(citations, 1):
    print(f"{i}. {citation['title']}")
    print(f"   {citation['url']}")
```

## Error Handling

### Handle Search Failures

```python
def safe_grounded_search(query, fallback=None):
    """Perform search with fallback."""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=query,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search={})]
            )
        )
        return response.text
        
    except Exception as e:
        print(f"Search failed: {e}")
        
        if fallback:
            # Try without grounding
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=query
            )
            return f"[Without grounding] {response.text}"
        
        return None

# Usage
result = safe_grounded_search(
    "Latest AI news",
    fallback=True
)
```

## Best Practices

1. **Use for current information**: Search is best for recent/live data
2. **Verify sources**: Check the grounding metadata
3. **Clear queries**: Formulate specific search queries
4. **Cite sources**: Always acknowledge grounded information
5. **Handle failures**: Implement fallback strategies
6. **Combine tools**: Use with code execution, function calling
7. **Iterative research**: Break down complex topics
8. **Check recency**: Verify information is up-to-date

## Complete Example

```python
class ResearchAgent:
    """Complete research agent with grounding."""
    
    def __init__(self):
        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "tools": [types.Tool(google_search={})],
                "system_instruction": """You are a research assistant.
                Use Google Search to find accurate, current information.
                Always cite your sources.
                Synthesize information from multiple sources.
                """
            }
        )
    
    def research(self, topic):
        """Research a topic thoroughly."""
        
        prompt = f"""Research this topic: {topic}
        
        Provide:
        1. Overview
        2. Key findings (with sources)
        3. Recent developments
        4. Relevant statistics
        5. Expert opinions
        """
        
        response = self.chat.send_message(prompt)
        
        # Extract citations
        citations = []
        if hasattr(response, 'grounding_metadata'):
            metadata = response.grounding_metadata
            if hasattr(metadata, 'grounding_chunks'):
                for chunk in metadata.grounding_chunks:
                    if hasattr(chunk, 'web'):
                        citations.append({
                            'title': chunk.web.title,
                            'url': chunk.web.uri
                        })
        
        return {
            'content': response.text,
            'citations': citations
        }
    
    def fact_check(self, claim):
        """Fact-check a claim."""
        
        prompt = f"""Fact-check this claim: "{claim}"
        
        Provide:
        1. Verdict (True/False/Uncertain)
        2. Evidence from reliable sources
        3. Context
        4. Sources
        """
        
        response = self.chat.send_message(prompt)
        return response.text
    
    def summarize_news(self, topic, num_articles=5):
        """Summarize recent news on a topic."""
        
        prompt = f"""Find and summarize the {num_articles} most recent news articles about: {topic}
        
        For each article:
        - Title
        - Source
        - Brief summary
        - Date (if available)
        """
        
        response = self.chat.send_message(prompt)
        return response.text

# Usage
agent = ResearchAgent()

# Research
result = agent.research("Quantum computing applications")
print(result['content'])
print("\nSources:")
for citation in result['citations']:
    print(f"- {citation['title']}: {citation['url']}")

# Fact-check
verdict = agent.fact_check("The Earth is flat")
print(verdict)

# News summary
news = agent.summarize_news("artificial intelligence", num_articles=5)
print(news)
```

## Real-World Use Cases

### Market Research Agent

```python
system_instruction = """You are a market research agent.
Research market trends, competitor information, and industry news.
Provide data-driven insights."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(google_search={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message("""
Research the electric vehicle market:
1. Top 5 manufacturers
2. Market share
3. Recent trends
4. Price ranges
""")
```

### Academic Research Assistant

```python
system_instruction = """You are an academic research assistant.
Find scholarly information and recent publications.
Focus on peer-reviewed sources."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(google_search={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message("""
Find recent research papers about:
"machine learning for drug discovery"

Summarize the key findings and methodologies.
""")
```

## Next Steps

- [Function Calling](function-calling.md) - Combine with custom tools
- [ReAct Pattern](../workflows/react-pattern.md) - Build reasoning agents
- [Multi-Turn Conversations](../workflows/multi-turn.md) - Iterative research
