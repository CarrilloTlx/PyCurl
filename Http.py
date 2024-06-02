# Curl/Http.py
import requests
import logging
import json
import os
from datetime import datetime
from ftplib import FTP, error_perm
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Http:
    """
    A class for making HTTP requests using the Python requests library.
    """
    base_url = ""

    def __init__(self):
        """
        Initializes a new instance of the Http class.

        Parameters:
        - base_url (str): The base URL for requests. Defaults to None.

        Attributes:
        - session (requests.Session): The requests session used for making requests.
        - headers (dict): Dictionary to store custom headers for requests.
        - cookies (dict): Dictionary to store cookies for requests.
        - auth (tuple): Tuple for storing basic authentication credentials (username, password).
        - timeout (int): Timeout in seconds for requests.
        - follow_redirects (bool): Flag to indicate whether to follow redirects.
        - _error_message (str): Stores the error message from the last failed request.
        - _error_code (int): Stores the error code from the last failed request.
        """
        self.session = requests.Session()
        self.headers = {}
        self.cookies = {}
        self.auth = None
        self.timeout = None
        self.follow_redirects = True
        self._error_message = None
        self._error_code = None

    def set_timeout(self, timeout):
        """
        Sets the timeout for requests.

        Parameters:
        - timeout (int): Timeout in seconds.
        """
        self.timeout = timeout

    def set_referer(self, referer):
        """
        Sets the Referer header for requests.

        Parameters:
        - referer (str): The referer URL.
        """
        self.set_header('Referer', referer)

    def set_header(self, key, value):
        """
        Sets a custom header for requests.

        Parameters:
        - key (str): The header name.
        - value (str): The header value.
        """
        self.headers[key] = value

    def set_basic_auth(self, username, password):
        """
        Sets basic authentication for requests.

        Parameters:
        - username (str): The username.
        - password (str): The password.
        """
        self.auth = (username, password)

    def set_bearer_auth(self, token):
        """
        Sets Bearer Token authentication for requests.

        Parameters:
        - token (str): The Bearer token.
        """
        self.set_header('Authorization', f'Bearer {token}')

    def set_user_agent(self, user_agent):
        """
        Sets the User-Agent for requests.

        Parameters:
        - user_agent (str): The User-Agent value.
        """
        self.set_header('User-Agent', user_agent)

    def set_follow_redirects(self, follow=True):
        """
        Sets whether to follow redirects.

        Parameters:
        - follow (bool): True to follow redirects, False otherwise. Defaults to True.
        """
        self.follow_redirects = follow

    def set_cookie(self, name, value):
        """
        Sets a cookie for requests.

        Parameters:
        - name (str): The cookie name.
        - value (str): The cookie value.
        """
        self.cookies[name] = value

    def _save_cookies(self, cookies):
        """
        Saves cookies to a JSON file.

        Parameters:
        - cookies (requests.cookies.RequestsCookieJar): The cookies to save.
        """
        try:
            try:
                with open('cookies.json', 'r') as file:
                    existing_cookies = json.load(file)
            except (IOError, json.JSONDecodeError):
                existing_cookies = {}

            new_cookies = requests.utils.dict_from_cookiejar(cookies)
            all_cookies = {**existing_cookies, **new_cookies}

            with open('cookies.json', 'w') as file:
                json.dump(all_cookies, file)

            logger.info("Cookies saved to file 'cookies.json'")
        except IOError as e:
            logger.error(f"Error saving cookies to file: {e}")

    def _request(self, method, url, **kwargs):
        """
        Makes an HTTP request using the specified method.

        Parameters:
        - method (str): The HTTP method (GET, POST, etc.).
        - url (str): The URL to make the request to.
        - **kwargs: Additional arguments for the request.

        Returns:
        - The response of the request, in JSON format if the content is JSON, otherwise as text.

        Raises:
        - requests.exceptions.RequestException: If there is an error in the request.
        """
        try:
            try:
                with open('cookies.json', 'r') as file:
                    saved_cookies = json.load(file)
            except (IOError, json.JSONDecodeError):
                saved_cookies = {}

            combined_cookies = {**saved_cookies, **self.cookies}

            kwargs.update({
                'headers': self.headers,
                'auth': self.auth,
                'timeout': self.timeout,
                'allow_redirects': self.follow_redirects,
                'cookies': combined_cookies
            })

            self._error_message = None
            self._error_code = None
            self.base_url = url

            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            self._save_cookies(response.cookies)
            return response.json() if 'application/json' in response.headers.get('content-type', '') else response.text
        except requests.exceptions.RequestException as e:
            self._error_message = str(e)
            self._error_code = getattr(e.response, 'status_code', None)
            logger.error(f"{method.upper()} request to {url} failed: {self._error_message} (code: {self._error_code})")
            raise

    def get(self, url, params=None):
        """
        Makes a GET request.

        Parameters:
        - url (str): The URL to make the request to.
        - params (dict): Query parameters. Defaults to None.

        Returns:
        - The response of the request.
        """
        return self._request('get', url, params=params)

    def post(self, url, data=None):
        """
        Makes a POST request.

        Parameters:
        - url (str): The URL to make the request to.
        - data (dict): Data to send in the request. Defaults to None.

        Returns:
        - The response of the request.
        """
        return self._request('post', url, json=data)

    def put(self, url, data=None):
        """
        Makes a PUT request.

        Parameters:
        - url (str): The URL to make the request to.
        - data (dict): Data to send in the request. Defaults to None.

        Returns:
        - The response of the request.
        """
        return self._request('put', url, json=data)

    def delete(self, url):
        """
        Makes a DELETE request.

        Parameters:
        - url (str): The URL to make the request to.

        Returns:
        - The response of the request.
        """
        return self._request('delete', url)

    def upload_ftp(self, host, username, password, file_path, upload_dir, port=21, passive=True):
        """
        Uploads a file to an FTP server and shows the progress.

        Parameters:
        - host (str): The FTP server host.
        - username (str): The username for authentication.
        - password (str): The password for authentication.
        - file_path (str): The path of the file to be uploaded.
        - upload_dir (str): The target directory on the FTP server.
        - port (int): The port to connect to on the FTP server. Default is 21.
        - passive (bool): Whether to use passive mode. Default is True.

        Returns:
        - str: The full path where the file was uploaded on the FTP server.
        """
        # Set up logging
        logging.basicConfig(level=logging.INFO)

        # Input validation
        if not os.path.isfile(file_path):
            logging.error(f"The file {file_path} does not exist.")
            return None

        try:
            # Connect to the FTP server
            ftp = FTP()
            ftp.connect(host, port)
            ftp.login(user=username, passwd=password)
            ftp.set_pasv(passive)
            logging.info(f"Connected to FTP server {host}:{port} with passive mode set to {passive}.")

            # Ensure the target directory exists, create if it does not
            try:
                ftp.cwd(upload_dir)
            except error_perm:
                logging.info(f"Directory {upload_dir} does not exist. Creating it.")
                try:
                    # Split the upload directory into parts and create each part if it doesn't exist
                    dirs = upload_dir.split('/')
                    current_dir = ''
                    for dir in dirs:
                        if dir:  # avoid empty parts
                            current_dir += f'/{dir}'
                            try:
                                ftp.cwd(current_dir)
                            except error_perm:
                                ftp.mkd(current_dir)
                                ftp.cwd(current_dir)
                except Exception as e:
                    logging.error(f"Failed to create directory {upload_dir}: {e}")
                    return None

            logging.info(f"Changed to directory {upload_dir} on FTP server.")

            # File size
            file_size = os.path.getsize(file_path)

            # Progress bar
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=os.path.basename(file_path), ascii=True,
                      colour='yellow') as pbar:
                def callback(data):
                    pbar.update(len(data))

                # Upload the file, overwriting if it already exists
                with open(file_path, 'rb') as file:
                    ftp.storbinary(f'STOR {os.path.basename(file_path)}', file, callback=callback)
                    logging.info(f"File {os.path.basename(file_path)} uploaded and overwritten successfully.")

            # Full path of the uploaded file
            uploaded_path = f"{upload_dir}/{os.path.basename(file_path)}"
            logging.info(f"File uploaded successfully to {uploaded_path}.")

            return uploaded_path

        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            return None

        finally:
            if 'ftp' in locals() and ftp.sock:
                ftp.quit()
                logging.info(f"Disconnected from FTP server {host}:{port}.")

    def download_large_file(self, url, method='get', params=None, chunk_size=8192, download_dir=None, file_name=None):
        """
        Downloads a large file and shows progress.

        Parameters:
        - url (str): The file URL.
        - method (str): The HTTP method (GET or POST). Defaults to 'get'.
        - params (dict): Request parameters. Defaults to None.
        - chunk_size (int): Chunk size for download. Defaults to 8192 bytes.
        - download_dir (str): Directory to save the file. Defaults to None.

        Returns:
        - The path to the downloaded file if the download completed successfully, None otherwise.
        """
        if not download_dir:
            print("No download directory provided. Download skipped.")
            return False

        try:
            start_time = datetime.now()

            if method.lower() == 'get':
                response = self.session.get(url, params=params, headers=self.headers, cookies=self.cookies,
                                            auth=self.auth, timeout=self.timeout, stream=True)
            elif method.lower() == 'post':
                response = self.session.post(url, json=params, headers=self.headers, cookies=self.cookies,
                                             auth=self.auth, timeout=self.timeout, stream=True)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            content_disposition = response.headers.get('content-disposition')
            if content_disposition:
                filename_index = content_disposition.find('filename=')
                if filename_index != -1:
                    filename = content_disposition[filename_index + len('filename='):]
                    filename = filename.strip('"')
                else:
                    filename = file_name
            else:
                filename = file_name

            downloaded_size = 0
            download_path = os.path.join(download_dir, filename)
            with open(download_path, 'wb') as file, tqdm(
                total=total_size, unit='B', unit_scale=True, desc=filename, ascii=True,
                bar_format='{l_bar}{bar:20}{r_bar}', colour='green'
            ) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        pbar.update(len(chunk))

            if os.path.exists(download_path):
                return download_path
            else:
                print("Downloaded file not found.")
                return None
        except requests.RequestException as e:
            print(f"Error downloading large file: {e}")
            return None

    def _format_size(self, size):
        """
        Formats the size in bytes to a human-readable string with appropriate unit.

        Parameters:
        - size (int): The size in bytes.

        Returns:
        - A tuple with the formatted size and unit.
        """
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return size, unit
            size /= 1024.0

    def reset(self):
        """
        Resets the HTTP client to its initial state.

        Parameters:
        - None

        Returns:
        - None
        """
        self.base_url = ""
        self.session.close()
        self.session = requests.Session()
        self.headers = {}
        self.cookies = {}
        self.auth = None
        self.timeout = None
        self.follow_redirects = True
        self._error_message = None
        self._error_code = None

    def get_error_message(self):
        """
        Gets the error message from the last failed request.

        Parameters:
        - None

        Returns:
        - The error message.
        """
        return self._error_message

    def get_error_code(self):
        """
        Gets the error code from the last failed request.

        Parameters:
        - None

        Returns:
        - The error code.
        """
        return self._error_code
