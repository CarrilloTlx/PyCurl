# PyCurlify


PyCurl is a Python package that provides a simple and flexible interface for making HTTP requests. It's designed to handle customizable configurations and error management, enabling easy execution of GET, POST, PUT, and DELETE requests.

## Key Features:
- Defines a base URL for all requests.
- Configures headers, cookies, and basic or token authentication.
- Handles redirects and timeouts.
- Manages and saves cookies to files.
- Extracts and manages HTTP response errors.
- Resets the HTTP client configuration to its initial state.

## Installation
You can install PyCurl using pip:

```
pip install PyCurlify
```

## Usage
```python
from Curl import PyCurlify

# Create an instance of PyCurl
http_client = PyCurl()

# Set the base URL
http_client.base_url = "https://api.example.com"

# Set headers
http_client.set_header('Authorization', 'Bearer my_token')

# Make a GET request
response = http_client.get("https://api.example.com/v1/endpoint")
print(response)
```

## Class `PyCurl`

### Methods

```python
__init__(self) 
```
Initializes a new instance of the `PyCurl` class.

```python
set_timeout(self, timeout)
```
Sets the timeout for requests.

```python
set_referer(self, referer)
```
Sets the Referer header for requests.

```python
set_header(self, key, value)
```
Sets a custom header for requests.

```python
set_basic_auth(self, username, password)
```
Sets basic authentication for requests.

```python
set_bearer_auth(self, token)
```
Sets Bearer token authentication for requests.

```python
set_user_agent(self, user_agent)
```
Sets the User-Agent for requests.

```python
set_follow_redirects(self, follow=True)
```
Sets whether to follow redirects.

```python
set_cookie(self, name, value)
```
Sets a cookie for requests.

```python
get(self, url, params=None)
```
Makes a GET request.

##### Parameters:
- `url` (str): The URL to make the request to.
- `params` (dict): Query parameters. Defaults to None.

##### Returns:
- The response of the request.

```python
post(self, url, data=None)
```
Makes a POST request.

##### Parameters:
- `url` (str): The URL to make the request to.
- `data` (dict): Data to send in the request. Defaults to None.

##### Returns:
- The response of the request.

```python
put(self, url, data=None)
```
Makes a PUT request.

##### Parameters:
- `url` (str): The URL to make the request to.
- `data` (dict): Data to send in the request. Defaults to None.

##### Returns:
- The response of the request.

```python
delete(self, url)
```
Makes a DELETE request.

##### Parameters:
- `url` (str): The URL to make the request to.

##### Returns:
- The response of the request.

```python
upload_ftp(self, host, username, password, file_path, upload_dir, port=21, passive=True)
```
Uploads a file to an FTP server and displays progress.

##### Parameters:
- `host` (str): The host of the FTP server.
- `username` (str): The username for authentication.
- `password` (str): The password for authentication.
- `file_path` (str): The path of the file to upload.
- `upload_dir` (str): The destination directory on the FTP server.
- `port` (int): The port to connect to on the FTP server. Defaults to 21.
- `passive` (bool): Whether to use passive mode. Defaults to True.

##### Returns:
- str: The full path where the file was uploaded on the FTP server.

```python
download_large_file(self, url, method='get', params=None, chunk_size=8192, download_dir=None, file_name=None)
```
Downloads a large file and displays progress.

##### Parameters:
- `url` (str): The URL of the file.
- `method` (str): The HTTP method (GET or POST). Defaults to 'get'.
- `params` (dict): Request parameters. Defaults to None.
- `chunk_size` (int): Chunk size for download. Defaults to 8192 bytes.
- `download_dir` (str): Directory to save the file. Defaults to None.

##### Returns:
- The path to the downloaded file if the download was successful, None otherwise.

```python
reset(self)
```
Resets the HTTP client to its initial state.

##### Returns:
- None

```python
get_error_message(self)
```
Gets the error message from the last failed request.

##### Returns:
- The error message.

```python
get_error_code(self)
```
Gets the error code from the last failed request.

##### Returns:
- The error code.


## Requirements

- requests
- tqdm

You can install these libraries using pip:

```
pip install requests tqdm
```

These libraries are required to run the code provided in this documentation.


## Contributions

Contributions are welcome! If you'd like to contribute to PyCurl, you can follow these steps:

1. Fork the repository from [here](https://github.com/CarrilloTlx/PyCurl).
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/PyCurl.git`
3. Create a branch for your contribution: `git checkout -b my-contribution`
4. Make your changes and commit: `git commit -am 'Add my contribution'`
5. Push your changes to your fork: `git push origin my-contribution`
6. Open a pull request in the original repository.

Thank you for contributing!

## License
This project is licensed under the Open Software License ("OSL") v 3.0. You can find the full text of the license [here](https://raw.githubusercontent.com/CarrilloTlx/PyCurl/main/LICENSE.md).