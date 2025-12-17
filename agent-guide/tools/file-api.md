# File API

## Overview

The File API allows you to upload files to Gemini for processing. This is essential for agents that need to work with documents, images, videos, and other media.

## Supported File Types

- **Images**: PNG, JPEG, WebP, HEIC, HEIF
- **Documents**: PDF, TXT
- **Audio**: WAV, MP3, AIFF, AAC, OGG, FLAC
- **Video**: MP4, MPEG, MOV, AVI, FLV, MPG, WebM, 3GPP

## Basic File Upload

### Upload a File

```python
from google import genai

client = genai.Client()

# Upload a file
uploaded_file = client.files.upload(path="/path/to/file.pdf")

print(f"Uploaded file: {uploaded_file.name}")
print(f"URI: {uploaded_file.uri}")
```

### Use Uploaded File

```python
# Generate content with the file
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        uploaded_file,
        "Summarize this document"
    ]
)

print(response.text)
```

## File Management

### List Files

```python
# List all uploaded files
for file in client.files.list():
    print(f"Name: {file.name}")
    print(f"Size: {file.size_bytes} bytes")
    print(f"State: {file.state}")
    print("---")
```

### Get File Details

```python
# Get specific file
file = client.files.get(name="files/abc123")

print(f"Display name: {file.display_name}")
print(f"MIME type: {file.mime_type}")
print(f"Created: {file.create_time}")
```

### Delete File

```python
# Delete a file when done
client.files.delete(name=uploaded_file.name)
print("File deleted")
```

## Working with Different File Types

### PDF Documents

```python
# Upload PDF
pdf_file = client.files.upload(path="document.pdf")

# Extract information
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        pdf_file,
        "Extract key information from this PDF"
    ]
)

print(response.text)
```

### Images

```python
# Upload image
image_file = client.files.upload(path="image.jpg")

# Analyze image
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        image_file,
        "Describe what you see in this image"
    ]
)

print(response.text)
```

### Audio Files

```python
# Upload audio
audio_file = client.files.upload(path="recording.mp3")

# Transcribe or analyze
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        audio_file,
        "Transcribe this audio and summarize the main points"
    ]
)

print(response.text)
```

### Video Files

```python
# Upload video
video_file = client.files.upload(path="video.mp4")

# Analyze video
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        video_file,
        "Describe what happens in this video"
    ]
)

print(response.text)
```

## Agent Use Cases

### Document Processing Agent

```python
class DocumentAgent:
    """Agent for processing documents."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def process_document(self, file_path, task):
        """Upload and process a document."""
        
        # Upload file
        uploaded_file = self.client.files.upload(path=file_path)
        
        # Wait for processing (for videos/audio)
        while uploaded_file.state == "PROCESSING":
            time.sleep(1)
            uploaded_file = self.client.files.get(name=uploaded_file.name)
        
        if uploaded_file.state == "FAILED":
            raise Exception("File processing failed")
        
        # Process with model
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, task]
        )
        
        # Clean up
        self.client.files.delete(name=uploaded_file.name)
        
        return response.text
    
    def extract_info(self, file_path):
        """Extract structured information."""
        
        return self.process_document(
            file_path,
            """Extract and return in JSON format:
            - Title
            - Author (if mentioned)
            - Key topics
            - Summary
            """
        )

# Usage
agent = DocumentAgent()
result = agent.extract_info("report.pdf")
print(result)
```

### Multi-File Analysis

```python
def analyze_multiple_files(file_paths, question):
    """Analyze multiple files together."""
    
    client = genai.Client()
    
    # Upload all files
    uploaded_files = []
    for path in file_paths:
        uploaded_file = client.files.upload(path=path)
        uploaded_files.append(uploaded_file)
    
    # Create content with all files
    contents = uploaded_files + [question]
    
    # Analyze
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    
    # Clean up
    for file in uploaded_files:
        client.files.delete(name=file.name)
    
    return response.text

# Usage
result = analyze_multiple_files(
    ["doc1.pdf", "doc2.pdf", "image.jpg"],
    "Compare these documents and image. What are the common themes?"
)
```

## File Processing States

### Handle Processing State

```python
import time

def wait_for_file_processing(client, file_name, timeout=300):
    """Wait for file to finish processing."""
    
    start_time = time.time()
    
    while True:
        file = client.files.get(name=file_name)
        
        if file.state == "ACTIVE":
            return file
        elif file.state == "FAILED":
            raise Exception("File processing failed")
        
        if time.time() - start_time > timeout:
            raise Exception("Processing timeout")
        
        time.sleep(2)

# Usage
uploaded_file = client.files.upload(path="video.mp4")
processed_file = wait_for_file_processing(client, uploaded_file.name)
```

## Streaming with Files

```python
# Upload file
file = client.files.upload(path="document.pdf")

# Stream response
for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=[file, "Summarize this document"]
):
    print(chunk.text, end="", flush=True)

# Clean up
client.files.delete(name=file.name)
```

## Error Handling

### Safe File Operations

```python
def safe_file_upload(client, file_path, max_size_mb=20):
    """Upload file with error handling."""
    
    import os
    
    try:
        # Check file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file size
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size > max_size_mb:
            raise ValueError(f"File too large: {file_size:.2f}MB > {max_size_mb}MB")
        
        # Upload
        uploaded_file = client.files.upload(path=file_path)
        return uploaded_file
        
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

# Usage
file = safe_file_upload(client, "document.pdf")
if file:
    # Process file
    pass
```

## Advanced Patterns

### Batch Processing

```python
def batch_process_files(file_paths, prompt_template):
    """Process multiple files in batch."""
    
    client = genai.Client()
    results = []
    
    for file_path in file_paths:
        try:
            # Upload
            uploaded_file = client.files.upload(path=file_path)
            
            # Process
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[uploaded_file, prompt_template]
            )
            
            results.append({
                "file": file_path,
                "result": response.text,
                "success": True
            })
            
            # Clean up
            client.files.delete(name=uploaded_file.name)
            
        except Exception as e:
            results.append({
                "file": file_path,
                "error": str(e),
                "success": False
            })
    
    return results

# Usage
results = batch_process_files(
    ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    "Extract the main conclusion from this document"
)
```

### File Caching for Repeated Use

```python
class FileCache:
    """Cache uploaded files for reuse."""
    
    def __init__(self, client):
        self.client = client
        self.cache = {}
    
    def get_or_upload(self, file_path):
        """Get cached file or upload new."""
        
        if file_path in self.cache:
            # Check if still valid
            try:
                file = self.client.files.get(name=self.cache[file_path])
                return file
            except:
                del self.cache[file_path]
        
        # Upload new
        uploaded_file = self.client.files.upload(path=file_path)
        self.cache[file_path] = uploaded_file.name
        return uploaded_file
    
    def cleanup(self):
        """Delete all cached files."""
        
        for file_name in self.cache.values():
            try:
                self.client.files.delete(name=file_name)
            except:
                pass
        
        self.cache.clear()

# Usage
cache = FileCache(client)

# First use - uploads
file1 = cache.get_or_upload("document.pdf")

# Second use - uses cached
file2 = cache.get_or_upload("document.pdf")

# Cleanup when done
cache.cleanup()
```

## Best Practices

1. **Delete files after use**: Free up storage
2. **Check file state**: Wait for processing to complete
3. **Handle errors**: Implement retry logic
4. **Validate file size**: Check before upload
5. **Use appropriate models**: Some models handle files better
6. **Batch processing**: Group similar files
7. **Cache when appropriate**: Reuse uploaded files
8. **Set timeouts**: Don't wait indefinitely

## Complete Example

```python
class FileProcessingAgent:
    """Complete file processing agent."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def process(self, file_path, task, cleanup=True):
        """Process a file with full error handling."""
        
        uploaded_file = None
        
        try:
            # Upload
            print(f"Uploading {file_path}...")
            uploaded_file = self.client.files.upload(path=file_path)
            
            # Wait for processing
            print("Processing...")
            start_time = time.time()
            while uploaded_file.state == "PROCESSING":
                if time.time() - start_time > 300:
                    raise Exception("Processing timeout")
                time.sleep(2)
                uploaded_file = self.client.files.get(name=uploaded_file.name)
            
            if uploaded_file.state == "FAILED":
                raise Exception("Processing failed")
            
            # Generate content
            print("Analyzing...")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[uploaded_file, task]
            )
            
            return response.text
            
        except Exception as e:
            print(f"Error: {e}")
            return None
            
        finally:
            # Cleanup
            if cleanup and uploaded_file:
                try:
                    self.client.files.delete(name=uploaded_file.name)
                    print("Cleaned up")
                except:
                    pass

# Usage
agent = FileProcessingAgent()
result = agent.process(
    "report.pdf",
    "Summarize the key findings and recommendations"
)
print(result)
```

## Next Steps

- [Function Calling](function-calling.md) - Combine with file processing
- [Code Execution](code-execution.md) - Analyze file data
- [Workflows](../workflows/) - Build complete file processing workflows
