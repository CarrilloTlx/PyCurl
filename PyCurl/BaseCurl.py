import xml.etree.ElementTree as ET
import base64
from urllib.parse import urlparse
import requests
import validators


class BaseCurl:
    def __init__(self):
        """
        Initializes a new instance of the BaseCurl class.

        BaseCurl provides a flexible wrapper around the requests library in Python,
        offering additional functionalities for making HTTP requests and handling responses.

        Attributes:
            before_send_callback: A callback function executed before sending a request.
            after_send_callback: A callback function executed after sending a request.
            success_callback: A callback function executed if the request is successful.
            error_callback: A callback function executed if the request encounters an error.
            complete_callback: A callback function executed after the request is complete.
        """
        self._stream = False
        self._session = requests.Session()
        self._follow_location = None
        self._headers = {}
        self._request_headers = {}
        self._cookies = {}
        self._timeout = None
        self._response = None
        self.before_send_callback = None
        self.after_send_callback = None
        self.success_callback = None
        self.error_callback = None
        self.complete_callback = None

    def disable_timeout(self):
        """
        Disable the timeout for the HTTP request.

        This method disables the timeout for the subsequent HTTP request. If the timeout is disabled, the request will not have a time limit and will wait indefinitely for a response.

        Parameters:
        None

        Returns:
        None
        """
        self.set_timeout(None)

    def set_timeout(self, seconds):
        """
        Set the timeout value for the HTTP request.

        This method sets the timeout value, in seconds, for the subsequent HTTP request. If the timeout is reached before the request is completed, a requests.Timeout exception will be raised.

        Parameters:
        - seconds (int or float): The timeout value in seconds. If set to None, the request will not have a timeout.

        Returns:
        None
        """
        self._timeout = seconds

    def set_user_agent(self, user_agent):
        """
        Set the 'User-Agent' header for the HTTP request.

        This method sets the 'User-Agent' header with the specified user agent string to be included in the HTTP request.

        Parameters:
        - user_agent (str): The user agent string to be set as the 'User-Agent' header.

        Returns:
        None
        """
        self.set_header("User-Agent", user_agent)

    def set_follow_location(self, follow_location=True):
        """
        Set the follow location setting for the HTTP request.

        This method allows enabling or disabling automatic following of HTTP redirects for the subsequent HTTP request.

        Parameters:
        - follow_location (bool, optional): A boolean flag indicating whether to follow HTTP redirects. Defaults to True.

        Returns:
        None
        """
        self._follow_location = follow_location

    def set_referer(self, referer):
        """
        Set the 'Referer' header for the HTTP request.

        This method sets the 'Referer' header with the specified referer URL to be included in the HTTP request.

        Parameters:
        - referer (str): The referer URL to be set as the 'Referer' header.

        Returns:
        None

        Raises:
        ValueError: If the provided referer URL is not a valid URL.
        """
        if validators.url(referer):
            self.set_header("Referer", referer)
        else:
            raise ValueError("Invalid referer URL")

    def set_header(self, key, value):
        """
        Set a single header for the HTTP request.

        This method sets a single header with the specified key and value to be included in the HTTP request.

        Parameters:
        - key (str): The key of the header.
        - value (str): The value of the header.

        Returns:
        None
        """
        self._headers[key] = value

    def set_headers(self, headers):
        """
        Set multiple headers for the HTTP request.

        This method sets multiple headers using a dictionary of key-value pairs to be included in the HTTP request.

        Parameters:
        - headers (dict): A dictionary containing the headers to be set, where keys are the header names and values are the corresponding header values.

        Returns:
        None
        """
        self._headers.update(headers)

    def remove_header(self, key):
        """
        Remove a header from the HTTP request.

        This method removes the header with the specified key from the headers to be included in the HTTP request.

        Parameters:
        - key (str): The key of the header to be removed.

        Returns:
        None
        """
        self._headers.pop(key, None)

    def get_request_headers(self):
        """
        Retrieve the headers sent in the last HTTP request.

        This method returns a copy of the headers sent in the last HTTP request made by the instance.

        Parameters:
        None

        Returns:
        dict: A dictionary containing the headers sent in the last HTTP request.

        Example:
        ```
        {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        ```
        """
        return self._request_headers.copy()

    def get_response_headers(self):
        """
        Retrieve the headers from the last HTTP response.

        This method returns a copy of the headers set in the last HTTP response received by the instance.

        Parameters:
        None

        Returns:
        dict or None: A dictionary containing the headers from the last HTTP response, if available. Otherwise, None.
        """
        if self._response:
            return self._response.headers.copy()
        return None

    def set_cookie(self, key, value):
        """
        Set a cookie for the HTTP request.

        This method sets a cookie with the specified key and value to be included in the HTTP request.

        Parameters:
        - key (str): The key of the cookie.
        - value (str): The value of the cookie.

        Returns:
        None
        """

    def set_cookies(self, cookies):
        """
            Set multiple cookies for the HTTP request.

            This method sets multiple cookies using a dictionary of key-value pairs to be included in the HTTP request.

            Parameters:
            - cookies (dict): A dictionary containing the cookies to be set, where keys are the cookie names and values are the corresponding cookie values.

            Returns:
            None
            """
        self._cookies.update(cookies)

    def set_cookie_string(self, string):
        """
        Set cookies using a string representation.

        This method parses the input string to extract individual cookie key-value pairs and sets the cookies accordingly.

        Parameters:
        - string (str): A string representation of cookies, where each key-value pair is separated by ';' and the key and value are separated by '='.

        Returns:
        None

        Raises:
        ValueError: If the input string is not in the expected format (i.e., key-value pairs separated by ';', and key and value separated by '=').
        """
        cookies = {}
        parts = string.split(';')
        for part in parts:
            key_value = part.strip().split('=', 1)
            if len(key_value) == 2:
                cookies[key_value[0]] = key_value[1]
            else:
                raise ValueError(f"Invalid cookie string: {string}")
        self.set_cookies(cookies)

    def get_cookies(self):
        """
            Retrieve the cookies from the last HTTP response.

            This method returns a copy of the cookies set in the last HTTP response received by the instance.

            Returns:
            dict: A dictionary containing the cookies from the last HTTP response.

            """
        return self.get_response().cookies.copy()

    def get_cookie(self, name):
        """
        Retrieve the value of a cookie from the last HTTP response.

        This method retrieves the value of a cookie with the specified name from the cookies set in the last HTTP response received by the instance.

        Parameters:
        - name (str): The name of the cookie to retrieve.

        Returns:
        str or None: The value of the cookie with the specified name if available in the last response, otherwise None.
        """
        response = self.get_response()
        if response:
            return response.cookies.get(name)
        return None

    def set_basic_authentication(self, username, password=''):
        """
        Set the Basic authentication header for the HTTP request.

        This method sets the Basic authentication header using the provided username and password.

        Parameters:
        - username (str): The username for Basic authentication.
        - password (str, optional): The password for Basic authentication. Defaults to an empty string.

        Returns:
        None
        """
        auth_string = f"{username}:{password}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes)
        auth_header = f"Basic {auth_base64.decode('utf-8')}"
        self.set_header('Authorization', auth_header)

    def set_bearer_authentication(self, token):
        """
        Set the Bearer token authentication header for the HTTP request.

        This method sets the Bearer token authentication header using the provided token.

        Parameters:
        - token (str): The Bearer token to be used for authentication.

        Returns:
        None
        """
        auth_header = f"Bearer {token}"
        self.set_header('Authorization', auth_header)

    def get_follow_location(self):
        """
        Retrieve the follow location setting for the HTTP request.

        This method returns the follow location setting for the HTTP request. If follow location is enabled, it returns True; otherwise, it returns False.

        Returns:
        bool: True if follow location is enabled, False if it is disabled or not set.
        """
        return self._follow_location

    def get_timeout(self):
        """
        Retrieve the timeout value for the HTTP request.

        This method returns the timeout value set for the HTTP request. If no timeout is set, it returns None.

        Returns:
        int or None: The timeout value in seconds, if set. Otherwise, None.
        """
        return self._timeout

    def get_response(self):
        """
        Retrieve the last HTTP response object.

        This method returns the last HTTP response object received by the instance. If there is no response available, it returns None.

        Returns:
        requests.Response or None: The last HTTP response object, if available. Otherwise, None.
        """
        return self._response

    def get_content(self):
        """
        Retrieve the raw content of the HTTP response.

        This method returns the raw content of the HTTP response received by the instance. If there is no response available, it raises a ValueError.

        Parameters:
        None

        Returns:
        bytes: The raw content of the HTTP response.

        Raises:
        ValueError: If there is no response available to retrieve the content from.
        """
        response = self.get_response()
        if response:
            return response.content
        else:
            raise ValueError("No hay ninguna respuesta disponible.")

    def response(self):
        """
        Process and return the content of the HTTP response based on its content type.

        This method checks the content type of the HTTP response and processes the content accordingly. If the content type is JSON, it attempts to return a JSON object. For HTML or XML content types, it returns the content as text. If the content type is XML, it tries to parse the XML and return an ElementTree object. If none of these conditions are met, it defaults to returning the raw content.

        Returns:
            - A JSON object if the content type is application/json and parsing is successful.
            - A string containing the response text if the content type is text/html or if JSON/XML parsing fails.
            - An ElementTree object if the content type is application/xml or text/xml and parsing is successful.
            - The raw response content for all other content types.

        Raises:
            ValueError: If there is no response available to process.
        """
        response = self.get_response()
        if response:
            content_type = response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                try:
                    return response.json()
                except ValueError:
                    # Si la conversión a JSON falla, devolvemos el contenido como texto
                    return response.text
            elif 'text/html' in content_type:
                return response.text
            elif 'application/xml' in content_type or 'text/xml' in content_type:
                try:
                    # Parseamos el contenido XML y devolvemos el objeto XML
                    return ET.fromstring(response.content)
                except ET.ParseError:
                    # Si el parsing falla, devolvemos el contenido como texto
                    return response.text
            else:
                return self.get_content()
        else:
            raise ValueError("No hay ninguna respuesta disponible.")

    def get_error_code(self):
        """
        Retrieve the HTTP status code from the last response as an error code.

        This method fetches the HTTP status code from the most recent HTTP response received by the instance. It is intended to be used for identifying error codes from HTTP responses. If there is no response available, it returns None.

        Parameters:
        None

        Returns:
        int or None: The HTTP status code of the response if available, otherwise None.
        """
        response = self.get_response()
        if response:
            return response.status_code
        return None

    def get_error_message(self):
        """
        Retrieve the error message from the last HTTP response.

        This method fetches the error message (reason phrase) from the most recent HTTP response received by the instance. If there is no response available, it returns None.

        Parameters:
        None

        Returns:
        str or None: The error message from the HTTP response if available, otherwise None.
        """
        response = self.get_response()
        if response:
            return response.reason
        return None

    def get_http_status_code(self):
        """
        Retrieve the HTTP status code from the last response.

        This method fetches the HTTP status code from the most recent HTTP response received by the instance. If there is no response available, it returns None.

        Parameters:
        None

        Returns:
        int or None: The HTTP status code of the response, if available. Otherwise, None.
        """
        response = self.get_response()
        if response:
            return response.status_code
        return None

    def get_http_error_message(self):
        """
        Get the HTTP error message from the response.

        This method retrieves the HTTP error message from the response object if available.

        Parameters:
        None

        Returns:
        str or None: The HTTP error message if available, or None if the response is not available.
        """
        response = self.get_response()
        if response:
            return response.reason
        return None

    def disable_stream(self):
        """
        Disable streaming for the HTTP request.

        This method disables streaming for the subsequent HTTP request. When streaming is disabled, the entire response content will be loaded into memory.

        Parameters:
        None

        Returns:
        None
        """
        self._stream = False

    def enable_stream(self):
        """
        Enable streaming for the HTTP request.

        This method enables streaming for the subsequent HTTP request. When streaming is enabled, the response content will be downloaded in chunks, allowing the processing of large responses without loading the entire content into memory.

        Parameters:
        None

        Returns:
        None
        """
        self._stream = True

    def exec(self, method, url, headers=None, cookies=None, params=None, data=None):
        """
        Execute an HTTP request using the specified method, URL, headers, cookies, params, and data.

        This method prepares and sends an HTTP request using the provided parameters, and handles the request lifecycle including callbacks.

        Parameters:
        - method (str): The HTTP method for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
        - url (str): The URL to which the request will be sent.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Parameters to be included in the query string.
        - data (dict, optional): The request payload data to be sent with the request.

        Returns:
        None

        Raises:
        Any exceptions raised during the request execution will be handled internally, and may trigger error or complete callbacks if provided.
        """
        parsed_url = urlparse(url)
        self.set_headers({
            ':scheme': parsed_url.scheme,
            ':path': parsed_url.path or '/',
            ':method': method.upper(),
            ':host': parsed_url.netloc,
            'Host': parsed_url.netloc,
            "Connection": "keep-alive"
        })

        final_headers = {**self._headers, **(headers or {})}
        final_cookies = {**self._cookies, **(cookies or {})}

        request_kwargs = {
            'method': method,
            'url': url,
            'headers': final_headers,
            'cookies': final_cookies,
            'timeout': self.get_timeout(),
            'allow_redirects': self.get_follow_location(),
            'params': params,  # Always include params for query string
            'stream': self._stream  # Enable streaming for response
        }

        if method.lower() in ['post', 'put', 'patch']:
            request_kwargs['json'] = data

        if self.before_send_callback:
            self.before_send_callback(request_kwargs)

        try:
            self._response = self._session.request(**request_kwargs)
        except requests.RequestException as e:
            if self.error_callback:
                self.error_callback(str(e))
            self.close()
            return

        self._request_headers = final_headers.copy()

        self.close()

        if self.after_send_callback:
            self.after_send_callback(self._response)

        if self._response.ok and self.success_callback:
            self.success_callback(self._response)
        elif self.error_callback:
            self.error_callback(self._response)

        if self.complete_callback:
            self.complete_callback(self._response)

    def close(self):
        """
        Close the current session and reset the instance attributes.

        This method resets the instance attributes related to session management, such as follow location, headers, cookies, and timeout.
        After calling this method, the instance can be re-used for making new requests with a clean state.

        Parameters:
        None

        Returns:
        None
        """
        self._follow_location = None
        self._headers = {}
        self._cookies = {}
        self._timeout = None
