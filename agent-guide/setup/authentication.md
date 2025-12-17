# Authentication

## Overview

The Gemini API uses API keys for authentication. This guide walks you through creating an API key and using it with the Python SDK or command-line tools.

## Create an API Key

You can [create your API key](https://aistudio.google.com/app/apikey) using Google AI Studio with a single click.

**Important:** Treat your API key like a password. Never commit it to source control or share it publicly.

## Setup Methods

### Method 1: Environment Variable (Recommended)

Set your API key as an environment variable in your terminal:

```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
```

Then use it in your Python code:

```python
import os
from google import genai

# Option 1: Explicit API key
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# Option 2: Automatic detection (looks for GOOGLE_API_KEY environment variable)
client = genai.Client()
```

### Method 2: Google Colab Secrets

If using Google Colab:

1. Click the 🔑 **Secrets** tab in the left panel
2. Create a new secret named `GOOGLE_API_KEY`
3. Paste your API key in the Value field
4. Enable access for all notebooks

Then access it in your notebook:

```python
from google import genai
from google.colab import userdata

GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)
```

## Installation

Install the Python SDK:

```bash
pip install -qU 'google-genai>=1.0.0'
```

## Test Your Setup

Verify your authentication works:

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello! Please respond with a greeting."
)

print(response.text)
```

## Using with cURL

For command-line usage:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{
          "text": "Hello! Please respond with a greeting."
        }]
      }]
    }'
```

## Security Best Practices

- Never hardcode API keys in source code
- Use environment variables or secure secret management
- Rotate keys regularly
- Use separate keys for development and production
- Monitor API usage for anomalies

## Next Steps

- [Installation Guide](installation.md) - Set up your development environment
- [Configuration](configuration.md) - Configure the SDK for your needs
- [Core Prompting](../core/prompting.md) - Learn how to interact with models
