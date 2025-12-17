# JSON Mode - Structured Outputs

## Overview

JSON mode enables you to request structured, parseable responses from the Gemini API. This is essential for agents that need to extract, process, or store data in a consistent format.

## Basic JSON Mode

### Simple JSON Response

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="List 3 programming languages with their use cases",
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)

import json
data = json.loads(response.text)
print(json.dumps(data, indent=2))
```

## With Schema Definition

### Define Structure

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Extract information about Python as a programming language",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "year_created": {"type": "integer"},
                "creator": {"type": "string"},
                "use_cases": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "popularity": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            },
            "required": ["name", "creator"]
        }
    )
)

data = json.loads(response.text)
print(json.dumps(data, indent=2))
```

### Expected Output

```json
{
  "name": "Python",
  "year_created": 1991,
  "creator": "Guido van Rossum",
  "use_cases": [
    "Web development",
    "Data science",
    "Machine learning",
    "Automation"
  ],
  "popularity": "high"
}
```

## Common Use Cases

### 1. Entity Extraction

```python
def extract_entities(text):
    """Extract structured entities from text"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Extract entities from this text: {text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "people": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "organizations": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "locations": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "dates": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        )
    )
    
    return json.loads(response.text)

# Usage
text = "John Smith met with Microsoft executives in New York on January 15th"
entities = extract_entities(text)
print(entities)
```

### 2. Sentiment Analysis

```python
def analyze_sentiment(text):
    """Analyze sentiment with structured output"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Analyze sentiment: {text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "negative", "neutral"]
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "key_phrases": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "emotions": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["joy", "anger", "sadness", "fear", "surprise"]
                        }
                    }
                },
                "required": ["sentiment", "confidence"]
            }
        )
    )
    
    return json.loads(response.text)

# Usage
result = analyze_sentiment("This product exceeded my expectations!")
print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']}")
```

### 3. Task Decomposition

```python
def decompose_task(task_description):
    """Break down a task into structured steps"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Break down this task: {task_description}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "task_name": {"type": "string"},
                    "estimated_time": {"type": "string"},
                    "difficulty": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard"]
                    },
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "step_number": {"type": "integer"},
                                "description": {"type": "string"},
                                "dependencies": {
                                    "type": "array",
                                    "items": {"type": "integer"}
                                }
                            }
                        }
                    },
                    "required_tools": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        )
    )
    
    return json.loads(response.text)

# Usage
task = "Deploy a Python web application to production"
plan = decompose_task(task)
for step in plan['steps']:
    print(f"{step['step_number']}. {step['description']}")
```

### 4. Data Classification

```python
def classify_text(text, categories):
    """Classify text into predefined categories"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Classify this text: {text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "primary_category": {
                        "type": "string",
                        "enum": categories
                    },
                    "secondary_categories": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": categories
                        }
                    },
                    "confidence_scores": {
                        "type": "object",
                        "additionalProperties": {"type": "number"}
                    },
                    "reasoning": {"type": "string"}
                },
                "required": ["primary_category"]
            }
        )
    )
    
    return json.loads(response.text)

# Usage
categories = ["technology", "business", "health", "entertainment", "sports"]
result = classify_text(
    "Apple announces new AI chip for data centers",
    categories
)
print(f"Category: {result['primary_category']}")
```

## Complex Schemas

### Nested Objects

```python
schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                        "country": {"type": "string"}
                    }
                }
            }
        },
        "orders": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "amount": {"type": "number"},
                    "items": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    }
}

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Generate sample customer data",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schema
    )
)
```

### Arrays of Objects

```python
def extract_products(page_text):
    """Extract product information from text"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Extract all products: {page_text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "price": {"type": "number"},
                                "currency": {"type": "string"},
                                "in_stock": {"type": "boolean"},
                                "features": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["name", "price"]
                        }
                    }
                }
            }
        )
    )
    
    return json.loads(response.text)
```

## Agent Integration

### ReAct Agent with JSON

```python
def react_agent_step(thought, available_actions):
    """Agent reasoning step with structured output"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Current thought: {thought}\nAvailable actions: {available_actions}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "reasoning": {"type": "string"},
                    "action": {
                        "type": "string",
                        "enum": available_actions
                    },
                    "action_input": {"type": "string"},
                    "confidence": {"type": "number"},
                    "should_continue": {"type": "boolean"}
                },
                "required": ["reasoning", "action", "should_continue"]
            }
        )
    )
    
    return json.loads(response.text)

# Usage
step = react_agent_step(
    "I need to find information about quantum computing",
    ["search", "calculate", "finish"]
)
print(f"Action: {step['action']}")
print(f"Reasoning: {step['reasoning']}")
```

### Decision Making

```python
def make_decision(context, options):
    """Make a structured decision"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Context: {context}\nOptions: {options}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "chosen_option": {"type": "string"},
                    "reasoning": {"type": "string"},
                    "pros": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "cons": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "confidence": {"type": "number"},
                    "alternative_suggestions": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["chosen_option", "reasoning"]
            }
        )
    )
    
    return json.loads(response.text)
```

## Error Handling

### Validation

```python
import json
from jsonschema import validate, ValidationError

def safe_json_extraction(prompt, schema):
    """Extract JSON with validation"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )
        
        data = json.loads(response.text)
        
        # Validate against schema
        validate(instance=data, schema=schema)
        
        return data
        
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None
    except ValidationError as e:
        print(f"Schema validation failed: {e}")
        return None
```

### Retry with Correction

```python
def extract_with_retry(prompt, schema, max_attempts=3):
    """Retry extraction if format is incorrect"""
    
    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema
                )
            )
            
            data = json.loads(response.text)
            return data
            
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt < max_attempts - 1:
                prompt += f"\n\nError: {e}. Please provide valid JSON."
            else:
                raise
    
    return None
```

## Best Practices

1. **Define clear schemas**: Be specific about types and constraints
2. **Use enums**: Limit string values to predefined options
3. **Mark required fields**: Specify which fields are mandatory
4. **Validate responses**: Always validate JSON against schema
5. **Handle errors**: Implement retry logic for malformed JSON
6. **Keep schemas simple**: Avoid overly complex nested structures
7. **Provide examples**: Include example JSON in prompts when needed

## Common Patterns

### Template Schema

```python
# Reusable schema template
ENTITY_SCHEMA = {
    "type": "object",
    "properties": {
        "entity_type": {"type": "string"},
        "name": {"type": "string"},
        "attributes": {
            "type": "object",
            "additionalProperties": True
        },
        "confidence": {"type": "number"}
    },
    "required": ["entity_type", "name"]
}
```

### Schema Builder

```python
def build_extraction_schema(fields):
    """Dynamically build extraction schema"""
    
    properties = {}
    for field_name, field_type in fields.items():
        properties[field_name] = {"type": field_type}
    
    return {
        "type": "object",
        "properties": properties
    }

# Usage
schema = build_extraction_schema({
    "title": "string",
    "author": "string",
    "year": "integer",
    "rating": "number"
})
```

## Next Steps

- [Error Handling](error-handling.md) - Handle API errors
- [Function Calling](../tools/function-calling.md) - Combine with tools
- [ReAct Pattern](../workflows/react-pattern.md) - Use in agent workflows
