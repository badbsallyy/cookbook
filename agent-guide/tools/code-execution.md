# Code Execution

## Overview

Code Execution allows Gemini to write and execute Python code to solve problems, perform calculations, process data, and generate visualizations. This is particularly powerful for data analysis agents.

## Basic Usage

### Enable Code Execution

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Calculate the fibonacci sequence up to 100",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

print(response.text)
```

### Simple Calculation

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is 12345 * 67890?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

print(response.text)
```

## Use Cases

### Mathematical Calculations

```python
prompt = """Calculate the following:
1. Sum of squares from 1 to 100
2. Factorial of 20
3. Prime numbers between 1 and 50
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

print(response.text)
```

### Data Analysis

```python
prompt = """Analyze this data and provide statistics:

Sales data: [120, 150, 180, 130, 190, 200, 175, 165]

Calculate:
- Mean
- Median
- Standard deviation
- Trend (increasing/decreasing)
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

print(response.text)
```

### Data Transformation

```python
prompt = """Transform this CSV data:

name,age,city
John,25,NYC
Jane,30,LA
Bob,35,SF

Tasks:
1. Sort by age
2. Filter people over 28
3. Count by city
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

print(response.text)
```

## Accessing Execution Results

### View Generated Code

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Calculate prime numbers up to 20",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

# Iterate through response parts
for candidate in response.candidates:
    for part in candidate.content.parts:
        if hasattr(part, 'executable_code'):
            print("Generated Code:")
            print(part.executable_code.code)
        if hasattr(part, 'code_execution_result'):
            print("\nExecution Output:")
            print(part.code_execution_result.output)
```

## Agent Integration

### Data Analysis Agent

```python
system_instruction = """You are a data analysis agent.
Use code execution to:
- Process data
- Calculate statistics
- Generate insights
- Create visualizations

Always show your code and explain the results."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(code_execution={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message("""
Analyze this sales data:
Month: Jan, Feb, Mar, Apr, May
Sales: 1000, 1200, 1100, 1400, 1300

Provide:
1. Growth rate
2. Average monthly sales
3. Predicted sales for June
""")

print(response.text)
```

### Problem-Solving Agent

```python
system_instruction = """You are a problem-solving agent.
Break down complex problems into steps and use code execution when needed."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(code_execution={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message("""
A store offers a 20% discount on items over $100.
Calculate the final price for:
- Item A: $80
- Item B: $120
- Item C: $150
Including 8% tax on the discounted price.
""")

print(response.text)
```

## Advanced Patterns

### Iterative Analysis

```python
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(code_execution={})],
        "system_instruction": "You are a data scientist"
    }
)

# First analysis
response1 = chat.send_message("Generate 100 random numbers from normal distribution")
print(response1.text)

# Follow-up analysis
response2 = chat.send_message("Now calculate the mean, median, and plot a histogram")
print(response2.text)

# Further analysis
response3 = chat.send_message("Are there any outliers?")
print(response3.text)
```

### Combined Tools

```python
def fetch_data(source: str) -> str:
    """Fetch data from a source."""
    return "1,2,3,4,5,6,7,8,9,10"

# Combine function calling with code execution
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [
            fetch_data,
            types.Tool(code_execution={})
        ],
        "system_instruction": "Fetch data then analyze it with code execution"
    }
)

response = chat.send_message("Fetch data and calculate statistics")
print(response.text)
```

## Error Handling

### Handle Execution Errors

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Calculate 1/0",  # This will cause an error
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution={})]
    )
)

# Check for execution errors
for candidate in response.candidates:
    for part in candidate.content.parts:
        if hasattr(part, 'code_execution_result'):
            result = part.code_execution_result
            if result.outcome == "ERROR":
                print(f"Code execution error: {result.output}")
```

### Retry with Correction

```python
def execute_with_retry(prompt, max_attempts=3):
    """Execute code with automatic retry on errors."""
    
    for attempt in range(max_attempts):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution={})]
            )
        )
        
        # Check for errors
        has_error = False
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'code_execution_result'):
                    if part.code_execution_result.outcome == "ERROR":
                        has_error = True
                        error_msg = part.code_execution_result.output
                        prompt = f"{prompt}\n\nPrevious attempt failed with error: {error_msg}\nPlease fix and try again."
        
        if not has_error:
            return response
    
    return None

# Usage
response = execute_with_retry("Calculate complex analysis")
```

## Limitations

### What Code Execution Can Do

- ✅ Mathematical calculations
- ✅ Data processing
- ✅ Statistical analysis
- ✅ String manipulation
- ✅ List/dict operations
- ✅ Algorithm implementation

### What Code Execution Cannot Do

- ❌ File I/O operations
- ❌ Network requests
- ❌ External library imports (limited)
- ❌ System calls
- ❌ Long-running processes
- ❌ Large data processing

## Best Practices

1. **Clear instructions**: Specify what calculations you need
2. **Provide context**: Include sample data formats
3. **Check results**: Validate execution output
4. **Handle errors**: Implement retry logic
5. **Combine with functions**: Use with other tools
6. **Iterative refinement**: Build on previous results
7. **Explain code**: Ask model to explain generated code

## Example: Complete Analysis Agent

```python
class DataAnalysisAgent:
    """Agent that performs data analysis using code execution."""
    
    def __init__(self):
        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model="gemini-2.5-flash",
            config={
                "tools": [types.Tool(code_execution={})],
                "system_instruction": """You are a data analysis expert.
                Use code execution to:
                1. Process and clean data
                2. Calculate statistics
                3. Identify patterns
                4. Generate insights
                
                Always show your code and explain results clearly."""
            }
        )
    
    def analyze(self, data, question):
        """Analyze data and answer question."""
        
        prompt = f"""Data: {data}

Question: {question}

Please:
1. Process the data
2. Perform relevant calculations
3. Provide insights
4. Show your code
"""
        
        response = self.chat.send_message(prompt)
        return response.text
    
    def follow_up(self, question):
        """Ask follow-up question about previous analysis."""
        
        response = self.chat.send_message(question)
        return response.text

# Usage
agent = DataAnalysisAgent()

# Initial analysis
result = agent.analyze(
    data="[100, 120, 110, 130, 125, 140, 135]",
    question="What is the trend and average?"
)
print(result)

# Follow-up
result = agent.follow_up("What's the growth rate?")
print(result)
```

## Real-World Example

```python
system_instruction = """You are a financial analysis agent.
Use code execution to analyze financial data and provide insights."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [types.Tool(code_execution={})],
        "system_instruction": system_instruction
    }
)

response = chat.send_message("""
Stock prices for the last 10 days:
[100, 102, 98, 105, 107, 103, 109, 111, 108, 112]

Calculate:
1. Daily returns
2. Volatility (standard deviation of returns)
3. Maximum drawdown
4. Simple moving average (3-day)
5. Is this stock trending up or down?
""")

print(response.text)
```

## Next Steps

- [Function Calling](function-calling.md) - Combine with custom functions
- [File API](file-api.md) - Process file data
- [ReAct Pattern](../workflows/react-pattern.md) - Build reasoning agents
