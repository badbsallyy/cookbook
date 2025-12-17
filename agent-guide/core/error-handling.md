# Error Handling

## Overview

Robust error handling is critical for production agents. This guide covers common errors, handling strategies, and best practices for the Gemini API.

## Common API Errors

### Authentication Errors

```python
from google import genai
from google.api_core import exceptions

client = genai.Client(api_key="invalid-key")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Hello"
    )
except exceptions.Unauthenticated as e:
    print(f"Authentication failed: {e}")
    print("Please check your API key")
```

### Rate Limit Errors

```python
import time

def handle_rate_limit(func, max_retries=3):
    """Retry with exponential backoff on rate limits"""
    
    for attempt in range(max_retries):
        try:
            return func()
        except exceptions.ResourceExhausted as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 1
                print(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Max retries exceeded: {e}")

# Usage
result = handle_rate_limit(
    lambda: client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Your prompt"
    )
)
```

### Invalid Request Errors

```python
try:
    response = client.models.generate_content(
        model="invalid-model-name",
        contents="Hello"
    )
except exceptions.InvalidArgument as e:
    print(f"Invalid request: {e}")
except exceptions.NotFound as e:
    print(f"Model not found: {e}")
```

## Comprehensive Error Handler

```python
from google.api_core import exceptions
import time

class GeminiErrorHandler:
    """Comprehensive error handling for Gemini API"""
    
    def __init__(self, max_retries=3, base_delay=1):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def execute_with_retry(self, func, *args, **kwargs):
        """Execute function with retry logic"""
        
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
                
            except exceptions.ResourceExhausted as e:
                last_exception = e
                wait_time = self.base_delay * (2 ** attempt)
                print(f"Rate limit hit. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                
            except exceptions.ServiceUnavailable as e:
                last_exception = e
                wait_time = self.base_delay * (2 ** attempt)
                print(f"Service unavailable. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                
            except exceptions.DeadlineExceeded as e:
                last_exception = e
                print(f"Request timeout. Attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.base_delay)
                    
            except exceptions.InvalidArgument as e:
                # Don't retry invalid arguments
                print(f"Invalid argument: {e}")
                raise
                
            except exceptions.Unauthenticated as e:
                # Don't retry authentication errors
                print(f"Authentication failed: {e}")
                raise
                
            except Exception as e:
                last_exception = e
                print(f"Unexpected error: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.base_delay)
        
        raise Exception(f"Max retries exceeded. Last error: {last_exception}")

# Usage
handler = GeminiErrorHandler(max_retries=3)

result = handler.execute_with_retry(
    client.models.generate_content,
    model="gemini-2.5-flash",
    contents="Your prompt"
)
```

## Content Safety Errors

### Handle Safety Blocks

```python
def handle_safety_blocks(response):
    """Check for and handle content safety blocks"""
    
    if not response.candidates:
        print("Response blocked due to safety reasons")
        return None
    
    candidate = response.candidates[0]
    
    # Check finish reason
    if candidate.finish_reason == "SAFETY":
        print("Content filtered by safety settings")
        if hasattr(candidate, 'safety_ratings'):
            for rating in candidate.safety_ratings:
                print(f"  {rating.category}: {rating.probability}")
        return None
    
    return response.text

# Usage
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Your prompt"
    )
    text = handle_safety_blocks(response)
    if text:
        print(text)
except Exception as e:
    print(f"Error: {e}")
```

### Adjust Safety Settings

```python
from google.genai import types

def generate_with_custom_safety(prompt, safety_level="BLOCK_MEDIUM_AND_ABOVE"):
    """Generate content with custom safety settings"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT",
                        threshold=safety_level
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH",
                        threshold=safety_level
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold=safety_level
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold=safety_level
                    ),
                ]
            )
        )
        return response.text
    except Exception as e:
        print(f"Error with safety level {safety_level}: {e}")
        return None
```

## Timeout Handling

### Set Request Timeout

```python
from google.api_core import timeout

def generate_with_timeout(prompt, timeout_seconds=30):
    """Generate content with timeout"""
    
    try:
        # Create timeout object
        request_timeout = timeout.ExponentialTimeout(
            initial=timeout_seconds,
            maximum=timeout_seconds,
            multiplier=1.0
        )
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            timeout=timeout_seconds
        )
        return response.text
        
    except exceptions.DeadlineExceeded:
        print(f"Request timed out after {timeout_seconds}s")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
```

## Validation Errors

### Input Validation

```python
def validate_and_generate(prompt, max_length=10000):
    """Validate input before API call"""
    
    # Check prompt length
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    if len(prompt) > max_length:
        raise ValueError(f"Prompt too long: {len(prompt)} > {max_length}")
    
    # Check for prohibited content
    prohibited_terms = ["[LIST YOUR PROHIBITED TERMS]"]
    for term in prohibited_terms:
        if term.lower() in prompt.lower():
            raise ValueError(f"Prompt contains prohibited term: {term}")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        raise Exception(f"API error: {e}")

# Usage
try:
    result = validate_and_generate("Your prompt")
    print(result)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Response Validation

```python
import json

def validate_json_response(response):
    """Validate JSON response format"""
    
    if not response or not response.text:
        raise ValueError("Empty response")
    
    try:
        data = json.loads(response.text)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")

# Usage
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Generate JSON data",
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    data = validate_json_response(response)
    print(data)
except ValueError as e:
    print(f"Validation error: {e}")
```

## Agent-Specific Error Handling

### Function Call Errors

```python
def handle_function_call_errors(response):
    """Handle errors in function calling"""
    
    try:
        if not response.candidates:
            return None, "No candidates in response"
        
        candidate = response.candidates[0]
        
        if not candidate.content.parts:
            return None, "No parts in response"
        
        for part in candidate.content.parts:
            if hasattr(part, 'function_call'):
                # Validate function call
                func_call = part.function_call
                
                if not func_call.name:
                    return None, "Function call missing name"
                
                if not hasattr(func_call, 'args'):
                    return None, "Function call missing arguments"
                
                return func_call, None
        
        return None, "No function call found"
        
    except Exception as e:
        return None, f"Error parsing function call: {e}"

# Usage
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Search for Python tutorials",
    config=types.GenerateContentConfig(
        tools=[...]  # Your tools
    )
)

func_call, error = handle_function_call_errors(response)
if error:
    print(f"Error: {error}")
else:
    print(f"Function: {func_call.name}")
```

### Multi-Step Error Recovery

```python
class AgentWithRecovery:
    """Agent with error recovery"""
    
    def __init__(self, client):
        self.client = client
        self.error_count = 0
        self.max_errors = 3
    
    def execute_step(self, prompt):
        """Execute step with error recovery"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            self.error_count = 0  # Reset on success
            return response.text, None
            
        except Exception as e:
            self.error_count += 1
            
            if self.error_count >= self.max_errors:
                return None, "Max errors exceeded. Stopping agent."
            
            # Try recovery strategy
            recovery_prompt = f"""Previous attempt failed with error: {e}
            
Please try again with a simpler approach."""
            
            return self.execute_step(recovery_prompt)
    
    def run(self, task):
        """Run agent task with error handling"""
        
        result, error = self.execute_step(task)
        
        if error:
            print(f"Agent failed: {error}")
            return None
        
        return result

# Usage
agent = AgentWithRecovery(client)
result = agent.run("Complex task description")
```

## Logging and Monitoring

### Error Logger

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiWithLogging:
    """Gemini client with comprehensive logging"""
    
    def __init__(self, client):
        self.client = client
    
    def generate(self, prompt, model="gemini-2.5-flash"):
        """Generate with logging"""
        
        start_time = datetime.now()
        
        try:
            logger.info(f"Request started: {model}")
            logger.debug(f"Prompt: {prompt[:100]}...")
            
            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"Request successful: {duration:.2f}s")
            
            return response.text
            
        except exceptions.ResourceExhausted as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise
            
        except exceptions.InvalidArgument as e:
            logger.error(f"Invalid argument: {e}")
            logger.debug(f"Prompt that caused error: {prompt}")
            raise
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"Request failed after {duration:.2f}s: {e}")
            raise

# Usage
logged_client = GeminiWithLogging(client)
result = logged_client.generate("Your prompt")
```

## Best Practices

1. **Always use try-except blocks** for API calls
2. **Implement exponential backoff** for rate limits
3. **Don't retry on authentication errors** - fix the credentials
4. **Validate inputs** before making API calls
5. **Log errors** for debugging and monitoring
6. **Set reasonable timeouts** to prevent hanging
7. **Handle safety blocks** gracefully
8. **Provide user-friendly error messages**
9. **Implement circuit breakers** for repeated failures
10. **Monitor error rates** in production

## Production-Ready Example

```python
class ProductionGeminiClient:
    """Production-ready Gemini client with error handling"""
    
    def __init__(self, api_key, max_retries=3, timeout=30):
        self.client = genai.Client(api_key=api_key)
        self.max_retries = max_retries
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
    
    def generate(self, prompt, model="gemini-2.5-flash", **kwargs):
        """Generate with comprehensive error handling"""
        
        # Validate input
        if not prompt or len(prompt) > 100000:
            raise ValueError("Invalid prompt length")
        
        # Retry logic
        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # Check for safety blocks
                if not response.candidates:
                    self.logger.warning("Response blocked by safety")
                    return None
                
                return response.text
                
            except exceptions.ResourceExhausted:
                wait = 2 ** attempt
                self.logger.warning(f"Rate limited, waiting {wait}s")
                time.sleep(wait)
                
            except exceptions.DeadlineExceeded:
                self.logger.error(f"Timeout after {self.timeout}s")
                if attempt == self.max_retries - 1:
                    raise
                    
            except (exceptions.InvalidArgument, exceptions.Unauthenticated) as e:
                self.logger.error(f"Non-retryable error: {e}")
                raise
                
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(1)
        
        raise Exception("Max retries exceeded")

# Usage
client = ProductionGeminiClient(api_key=os.environ['GOOGLE_API_KEY'])
try:
    result = client.generate("Your prompt")
    print(result)
except Exception as e:
    print(f"Failed: {e}")
```

## Next Steps

- [Streaming](streaming.md) - Handle streaming errors
- [Function Calling](../tools/function-calling.md) - Error handling with tools
- [Models Guide](models.md) - Choose appropriate models
