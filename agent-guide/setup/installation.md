# Installation Guide

## Overview

This guide covers setting up your Python environment for developing agents with the Gemini API.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- A Google account
- An API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Python Environment Setup

### Option 1: Virtual Environment (Recommended)

Create an isolated Python environment:

```bash
# Create virtual environment
python -m venv gemini-env

# Activate on Linux/Mac
source gemini-env/bin/activate

# Activate on Windows
gemini-env\Scripts\activate
```

### Option 2: Conda Environment

If using Anaconda or Miniconda:

```bash
# Create conda environment
conda create -n gemini-env python=3.11

# Activate environment
conda activate gemini-env
```

## Install Core Dependencies

Install the Gemini Python SDK:

```bash
pip install -U google-genai
```

## Optional Dependencies

Depending on your use case, install additional packages:

### For Agent Development
```bash
pip install python-dotenv  # For environment variable management
```

### For Data Processing
```bash
pip install pandas numpy
```

### For Working with Documents
```bash
pip install PyPDF2 python-docx
```

### For Web Scraping (for ReAct agents)
```bash
pip install requests beautifulsoup4
```

### For Async Operations
```bash
pip install aiohttp asyncio
```

## Verify Installation

Test that everything is installed correctly:

```python
from google import genai
import sys

print(f"Python version: {sys.version}")
print(f"Genai module imported successfully")

# Test API connection (requires API key to be set)
try:
    client = genai.Client()
    print("✓ Client initialized successfully")
except Exception as e:
    print(f"✗ Client initialization failed: {e}")
```

## Environment Configuration

Create a `.env` file in your project root:

```bash
# .env
GOOGLE_API_KEY=your_api_key_here
```

Load environment variables in your code:

```python
from dotenv import load_dotenv
import os

load_dotenv()

from google import genai
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
```

## Project Structure

Recommended directory structure for agent projects:

```
my-agent-project/
├── .env                 # Environment variables (add to .gitignore!)
├── .gitignore          # Git ignore file
├── requirements.txt    # Python dependencies
├── agents/             # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py
│   └── tools.py
├── examples/           # Example scripts
│   └── simple_agent.py
└── tests/             # Test files
    └── test_agent.py
```

## requirements.txt Template

Create a `requirements.txt` file:

```
google-genai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

## IDE Setup

### VS Code

Install recommended extensions:
- Python (Microsoft)
- Jupyter (Microsoft)
- Python Docstring Generator

### PyCharm

Enable:
- Python type hints
- Code completion for Google APIs

## Troubleshooting

### Import Errors

If you encounter import errors:

```bash
pip install --upgrade pip
pip install --upgrade google-genai
```

### SSL Certificate Errors

On some systems, you may need to install certificates:

```bash
# macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# Or use pip
pip install certifi
```

### Permission Errors

On Linux/Mac, use pip with user flag:

```bash
pip install --user google-genai
```

## Next Steps

- [Authentication](authentication.md) - Set up your API key
- [Configuration](configuration.md) - Configure the SDK
- [Prompting Guide](../core/prompting.md) - Start building prompts
