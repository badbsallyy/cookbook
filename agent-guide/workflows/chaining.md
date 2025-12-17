# Prompt Chaining

## Overview

Prompt chaining breaks down complex tasks into a sequence of simpler prompts, where the output of one prompt becomes the input for the next. This improves quality, makes debugging easier, and enables sophisticated workflows.

## Basic Chaining

### Simple Two-Step Chain

```python
from google import genai

client = genai.Client()

# Step 1: Generate outline
outline_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Create a blog post outline about AI in healthcare"
)

outline = outline_response.text
print("Outline:")
print(outline)
print("\n" + "="*50 + "\n")

# Step 2: Expand outline into full post
article_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"Expand this outline into a full blog post:\n\n{outline}"
)

print("Full Article:")
print(article_response.text)
```

### Three-Step Chain

```python
def create_article(topic):
    """Create article through multi-step process."""
    
    # Step 1: Research
    research_prompt = f"Research and list key points about: {topic}"
    research = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=research_prompt
    ).text
    
    # Step 2: Create structure
    structure_prompt = f"Create a structured outline from these points:\n{research}"
    structure = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=structure_prompt
    ).text
    
    # Step 3: Write article
    article_prompt = f"Write a complete article based on this structure:\n{structure}"
    article = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=article_prompt
    ).text
    
    return {
        "research": research,
        "structure": structure,
        "article": article
    }

# Usage
result = create_article("Machine Learning in Finance")
print(result["article"])
```

## Sequential Processing

### Data Pipeline

```python
class DataProcessingChain:
    """Chain for data processing."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def extract(self, raw_data):
        """Extract structured data."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Extract key information from:\n{raw_data}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    
    def transform(self, data):
        """Transform data format."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Transform this data into a summary:\n{json.dumps(data)}"
        )
        return response.text
    
    def analyze(self, summary):
        """Analyze summary."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Provide insights from this summary:\n{summary}"
        )
        return response.text
    
    def process(self, raw_data):
        """Run full chain."""
        extracted = self.extract(raw_data)
        transformed = self.transform(extracted)
        analyzed = self.analyze(transformed)
        
        return {
            "extracted": extracted,
            "summary": transformed,
            "insights": analyzed
        }

# Usage
pipeline = DataProcessingChain()
result = pipeline.process("Sales data: 100 units in Jan, 150 in Feb...")
```

## Branching Chains

### Conditional Processing

```python
def process_with_branching(content, content_type):
    """Chain with conditional branching."""
    
    # Step 1: Classify
    if content_type == "article":
        # Article processing chain
        summary = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize this article:\n{content}"
        ).text
        
        keywords = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Extract keywords from:\n{summary}"
        ).text
        
        return {"type": "article", "summary": summary, "keywords": keywords}
    
    elif content_type == "data":
        # Data processing chain
        analysis = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze this data:\n{content}"
        ).text
        
        visualization = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Suggest visualizations for:\n{analysis}",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution={})]
            )
        ).text
        
        return {"type": "data", "analysis": analysis, "viz": visualization}
```

## Iterative Refinement

### Progressive Enhancement

```python
def iterative_refinement(initial_content, iterations=3):
    """Refine content through multiple iterations."""
    
    content = initial_content
    history = [{"iteration": 0, "content": content}]
    
    for i in range(iterations):
        # Critique
        critique = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Critique this content and suggest improvements:\n{content}"
        ).text
        
        # Improve
        improved = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Improve the content based on this critique:\n\nOriginal: {content}\n\nCritique: {critique}"
        ).text
        
        content = improved
        history.append({
            "iteration": i + 1,
            "critique": critique,
            "content": content
        })
    
    return history

# Usage
result = iterative_refinement("Write about AI", iterations=3)
for step in result:
    print(f"Iteration {step['iteration']}:")
    print(step.get('content', '')[:100])
    print()
```

## Parallel Chains

### Concurrent Processing

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_chain(topic, perspectives):
    """Process multiple chains in parallel."""
    
    def process_perspective(perspective):
        return client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Write about {topic} from {perspective} perspective"
        ).text
    
    # Process all perspectives in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_perspective, perspectives))
    
    # Synthesize results
    synthesis = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Synthesize these perspectives:\n\n" + "\n\n".join(results)
    ).text
    
    return {
        "perspectives": dict(zip(perspectives, results)),
        "synthesis": synthesis
    }

# Usage
result = parallel_chain(
    "artificial intelligence",
    ["technical", "ethical", "business"]
)
```

## Content Generation Chain

### Story Writing Workflow

```python
class StoryWriter:
    """Multi-step story generation."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def generate_characters(self, theme):
        """Step 1: Create characters."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Create 3 characters for a story about: {theme}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    
    def generate_plot(self, characters, theme):
        """Step 2: Create plot."""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Create a plot outline for theme '{theme}' with characters: {characters}"
        )
        return response.text
    
    def write_scenes(self, plot, num_scenes=3):
        """Step 3: Write scenes."""
        scenes = []
        for i in range(num_scenes):
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Write scene {i+1} based on this plot:\n{plot}"
            )
            scenes.append(response.text)
        return scenes
    
    def combine_story(self, scenes):
        """Step 4: Combine and polish."""
        combined = "\n\n".join(scenes)
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Polish and combine these scenes into a cohesive story:\n{combined}"
        )
        return response.text
    
    def write(self, theme):
        """Execute full chain."""
        characters = self.generate_characters(theme)
        plot = self.generate_plot(characters, theme)
        scenes = self.write_scenes(plot)
        story = self.combine_story(scenes)
        
        return {
            "characters": characters,
            "plot": plot,
            "scenes": scenes,
            "final_story": story
        }

# Usage
writer = StoryWriter()
story = writer.write("time travel")
print(story["final_story"])
```

## Error Handling in Chains

### Resilient Chain

```python
class ResilientChain:
    """Chain with error recovery."""
    
    def __init__(self, steps, max_retries=3):
        self.client = genai.Client()
        self.steps = steps
        self.max_retries = max_retries
    
    def execute_step(self, step_func, input_data, step_name):
        """Execute a single step with retry."""
        
        for attempt in range(self.max_retries):
            try:
                result = step_func(input_data)
                return {"success": True, "result": result}
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"Step '{step_name}' failed, retrying...")
                else:
                    return {"success": False, "error": str(e)}
        
    def run(self, initial_input):
        """Run chain with error handling."""
        
        results = []
        current_input = initial_input
        
        for i, step_func in enumerate(self.steps):
            step_name = f"Step {i+1}"
            print(f"Executing {step_name}...")
            
            result = self.execute_step(step_func, current_input, step_name)
            
            if not result["success"]:
                print(f"Chain failed at {step_name}: {result['error']}")
                break
            
            results.append(result["result"])
            current_input = result["result"]
        
        return results

# Usage
def step1(input_data):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Process: {input_data}"
    ).text

def step2(input_data):
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Refine: {input_data}"
    ).text

chain = ResilientChain([step1, step2])
results = chain.run("Initial data")
```

## Advanced Patterns

### Dynamic Chain

```python
class DynamicChain:
    """Chain that adapts based on intermediate results."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def decide_next_step(self, current_result):
        """Decide which step to execute next."""
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Given this result:\n{current_result}\n\nWhat should we do next: analyze, summarize, or finish?"
        )
        
        decision = response.text.lower()
        
        if "analyze" in decision:
            return self.analyze
        elif "summarize" in decision:
            return self.summarize
        else:
            return None
    
    def analyze(self, data):
        """Analysis step."""
        return client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Analyze: {data}"
        ).text
    
    def summarize(self, data):
        """Summary step."""
        return client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize: {data}"
        ).text
    
    def run(self, initial_input, max_steps=5):
        """Run dynamic chain."""
        
        current_result = initial_input
        
        for i in range(max_steps):
            next_step = self.decide_next_step(current_result)
            
            if next_step is None:
                break
            
            current_result = next_step(current_result)
        
        return current_result
```

## Best Practices

1. **Clear step boundaries**: Each step has a single purpose
2. **Validate outputs**: Check results before passing to next step
3. **Error handling**: Implement retry and fallback logic
4. **Logging**: Track progress through the chain
5. **Parallelization**: Run independent steps concurrently
6. **Caching**: Store intermediate results
7. **Testing**: Test each step independently
8. **Modularity**: Make steps reusable

## Complete Example

```python
class ProductionChain:
    """Production-ready prompt chain."""
    
    def __init__(self):
        self.client = genai.Client()
        self.cache = {}
    
    def cached_step(self, key, func, *args):
        """Execute step with caching."""
        if key in self.cache:
            return self.cache[key]
        
        result = func(*args)
        self.cache[key] = result
        return result
    
    def run_content_pipeline(self, topic):
        """Complete content creation pipeline."""
        
        # Step 1: Research
        research = self.cached_step(
            f"research_{topic}",
            lambda t: self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Research key points about: {t}",
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search={})]
                )
            ).text,
            topic
        )
        
        # Step 2: Outline
        outline = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Create outline from:\n{research}"
        ).text
        
        # Step 3: Draft
        draft = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Write draft from outline:\n{outline}"
        ).text
        
        # Step 4: Edit
        final = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Edit and polish:\n{draft}"
        ).text
        
        return {
            "research": research,
            "outline": outline,
            "draft": draft,
            "final": final
        }

# Usage
chain = ProductionChain()
result = chain.run_content_pipeline("Quantum Computing")
print(result["final"])
```

## Next Steps

- [ReAct Pattern](react-pattern.md) - Add reasoning to chains
- [Multi-Turn](multi-turn.md) - Build conversational chains
- [Function Calling](../tools/function-calling.md) - Add tools to chains
