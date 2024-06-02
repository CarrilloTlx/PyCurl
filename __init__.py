# Curl/__init__.py

"""
Curl Package

The Curl package provides a simple and flexible interface for making HTTP requests in Python.
It is designed to handle customizable settings and error management, allowing for easy execution
of GET, POST, PUT, and DELETE requests.

Key Features:
- Define a base URL for all requests.
- Configure headers, cookies, and basic or token authentication.
- Handle redirects and timeouts.
- Manage and save cookies to files.
- Extract and manage errors from HTTP responses.
- Reset the HTTP client configuration to its initial state.

Usage example:
```python
from Curl import Http

http_client = Http(base_url="https://api.example.com")
http_client.set_header('Authorization', 'Bearer my_token')
response = http_client.get("/endpoint")
print(response)

"""

# Automatically import the Http class when the package is imported
from .Http import Http as PyCurl

# Define the symbols exported by the package
__all__ = ['PyCurl']

# Package version
__version__ = '1.0.0'

# Description of the package functionality
__description__ = "A package for handling HTTP requests with customizable settings and error handling."

# Optional global configuration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Curl package imported successfully")
