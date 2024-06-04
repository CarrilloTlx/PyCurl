"""
PyCurl - A flexible wrapper around the requests library for making HTTP requests.

PyCurl extends the functionality provided by BaseCurl to offer simplified methods for making common HTTP requests such as GET, POST, PUT, DELETE, PATCH, and OPTIONS.

Attributes:
    PyCurl.Curl: A class providing simplified methods for making HTTP requests.
    PyCurl.__version__: The version of the PyCurl package.
    PyCurl.__description__: A brief description of the PyCurl package.

Example Usage:
    from PyCurl import PyCurl

    curl = PyCurl()
    curl.get('https://api.example.com/data')
    response = curl.response()
    print(response)
"""

from .Curl import Curl as PyCurlify

__all__ = ['PyCurlify']

__version__ = '2.0.0'
__description__ = 'PyCurlify: A flexible wrapper around the requests library for making HTTP requests.'

# Additional imports
# from .utils import some_function
# from .config import CONFIG_VARIABLE

# Initialize global variables or resources
# SOME_GLOBAL_VAR = initialize_global_var()

# Document additional details
# INSTALLATION_NOTES = """
# To install PyCurl, you can use pip:
# pip install PyCurl
# """

# Exception handling
# try:
#     # Code that may raise exceptions
# except SomeException as e:
#     # Handle the exception

# Alias for classes or functions
# ShortCurl = PyCurl

# Configuration variables
# CONFIG_VARIABLE = 'default_value'
