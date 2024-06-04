import ftplib
import os
import asyncio
from tqdm import tqdm

from .BaseCurl import BaseCurl


class Curl(BaseCurl):
    """
    A class extending BaseCurl to provide simplified methods for making HTTP requests.

    Curl extends the functionality provided by BaseCurl to offer simplified methods for making common HTTP requests such as GET, POST, PUT, DELETE, PATCH, and OPTIONS.

    Attributes:
        Inherits all attributes from BaseCurl.

    Methods:
        __init__(self): Initializes a new instance of the Curl class.
        get(self, url, headers=None, cookies=None, params=None): Sends a GET request to the specified URL.
        post(self, url, headers=None, cookies=None, params=None, data=None): Sends a POST request to the specified URL with optional headers, cookies, and data.
        put(self, url, headers=None, cookies=None, params=None, data=None): Sends a PUT request to the specified URL with optional headers, cookies, and data.
        options(self, url, headers=None, cookies=None, params=None): Sends an OPTIONS request to the specified URL.
        delete(self, url, headers=None, cookies=None, params=None): Sends a DELETE request to the specified URL.
        patch(self, url, headers=None, cookies=None, params=None, data=None): Sends a PATCH request to the specified URL with optional headers, cookies, and data.

    Example Usage:
    ```
    curl = PyCurl()
    curl.get('https://api.example.com/data')
    response = curl.response()
    print(response)
    ```
    """

    def __init__(self):
        """
        Initializes a new instance of the Curl class.

        Parameters:
        None

        Returns:
        None
        """
        super().__init__()

    def get(self, url, headers=None, cookies=None, params=None):
        """
        Sends a GET request to the specified URL.

        This method sends a GET request to the provided URL with optional headers, cookies, and query parameters.

        Parameters:
        - url (str): The URL to which the GET request will be sent.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Query parameters to be included in the request.

        Returns:
        dict or None: A dictionary containing the response data, including status code, headers, and content,
                      or None if the request was not successful.

        Raises:
        Any exceptions raised during the request execution will be handled internally.
        """
        self.exec('get', url, headers=headers, cookies=cookies, params=params)
        return self.get_response()

    def post(self, url, headers=None, cookies=None, params=None, data=None):
        """
        Sends a POST request to the specified URL.

        This method sends a POST request to the provided URL with optional headers, cookies, query parameters, and data payload.

        Parameters:
        - url (str): The URL to which the POST request will be sent.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Query parameters to be included in the request.
        - data (dict, optional): The data payload to be sent with the request.

        Returns:
        dict or None: A dictionary containing the response data, including status code, headers, and content,
                      or None if the request was not successful.

        Raises:
        Any exceptions raised during the request execution will be handled internally.
        """
        self.exec('post', url, headers=headers, cookies=cookies, params=params, data=data)
        return self.get_response()

    def put(self, url, headers=None, cookies=None, params=None, data=None):
        """
        Sends a PUT request to the specified URL.

        This method sends a PUT request to the provided URL with optional headers, cookies, query parameters, and data payload.

        Parameters:
        - url (str): The URL to which the PUT request will be sent.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Query parameters to be included in the request.
        - data (dict, optional): The data payload to be sent with the request.

        Returns:
        dict or None: A dictionary containing the response data, including status code, headers, and content,
                      or None if the request was not successful.

        Raises:
        Any exceptions raised during the request execution will be handled internally.
        """
        self.exec('put', url, headers=headers, cookies=cookies, params=params, data=data)
        return self.get_response()

    def options(self, url, headers=None, cookies=None, params=None):
        """
        Sends an OPTIONS request to the specified URL.

        This method sends an OPTIONS request to the provided URL with optional headers, cookies, and query parameters.

        Parameters:
        - url (str): The URL to which the OPTIONS request will be sent.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Query parameters to be included in the request.

        Returns:
        dict or None: A dictionary containing the response data, including status code, headers, and content,
                      or None if the request was not successful.

        Raises:
        Any exceptions raised during the request execution will be handled internally.
        """
        self.exec('options', url, headers=headers, cookies=cookies, params=params)
        return self.get_response()

    def delete(self, url, headers=None, cookies=None, params=None):
        """
        Sends a DELETE request to the specified URL.

        This method sends a DELETE request to the provided URL with optional headers, cookies, and query parameters.

        Parameters:
        - url (str): The URL to which the DELETE request will be sent.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Query parameters to be included in the request.

        Returns:
        dict or None: A dictionary containing the response data, including status code, headers, and content,
                      or None if the request was not successful.

        Raises:
        Any exceptions raised during the request execution will be handled internally.
        """
        self.exec('delete', url, headers=headers, cookies=cookies, params=params)
        return self.get_response()

    def patch(self, url, headers=None, cookies=None, params=None, data=None):
        """
        Sends a PATCH request to the specified URL.

        This method sends a PATCH request to the provided URL with optional headers, cookies, query parameters, and data payload.

        Parameters:
        - url (str): The URL to which the PATCH request will be sent.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Query parameters to be included in the request.
        - data (dict, optional): The data payload to be sent with the request.

        Returns:
        dict or None: A dictionary containing the response data, including status code, headers, and content,
                      or None if the request was not successful.

        Raises:
        Any exceptions raised during the request execution will be handled internally.
        """
        self.exec('patch', url, headers=headers, cookies=cookies, params=params, data=data)
        return self.get_response()

    def download_file(self, url, dir_path, file_name, method='get', headers=None, cookies=None, params=None, data=None):
        """
        Downloads a file from the specified URL and saves it to the specified directory.

        Parameters:
        - url (str): The URL from which to download the file.
        - dir_path (str): The directory path where the file will be saved.
        - file_name (str): The name of the file to be saved.
        - method (str, optional): The HTTP method to use for the request. Defaults to 'get'.
        - headers (dict, optional): Additional headers to be included in the request.
        - cookies (dict, optional): Cookies to be included in the request.
        - params (dict, optional): Query parameters to be included in the request.
        - data (dict, optional): The data payload to be sent with the request.

        Returns:
        dict or None: A dictionary containing information about the downloaded file, including its path and size,
                      or None if the file could not be downloaded.

        Raises:
        FileNotFoundError: If the specified directory does not exist.
        ValueError: If an unsupported HTTP method is provided. Only 'get' and 'post' are supported.
        """
        try:
            # Check if the specified directory exists
            if not os.path.exists(dir_path):
                raise FileNotFoundError(f"The specified directory '{dir_path}' does not exist.")

            # Create the full file path
            file_path = os.path.join(dir_path, file_name)

            # Enable streaming for the request
            self.enable_stream()

            # Perform the HTTP request
            if method.lower() == 'get':
                response = self.get(url, headers=headers, cookies=cookies, params=params)
            elif method.lower() == 'post':
                response = self.post(url, headers=headers, cookies=cookies, params=params, data=data)
            else:
                raise ValueError("Unsupported HTTP method. Only 'get' and 'post' are supported.")

            # Get the total size of the file to download
            total_size = int(response.headers.get('content-length', 0))

            # Write the downloaded data to the file while displaying a progress bar
            with open(file_path, 'wb') as file, tqdm(
                    desc="Downloading",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    bar_format="{l_bar}{bar}{r_bar}",
                    colour='green'
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    bar.update(len(data))

            # Check if the file was successfully downloaded
            if os.path.exists(file_path):
                # Disable streaming after the download is complete
                self.disable_stream()
                # Return information about the downloaded file
                return {'file_path': file_path, 'file_size': total_size}
            else:
                # Disable streaming if the file could not be downloaded
                self.disable_stream()
                return None
        except Exception as e:
            # Disable streaming in case of any exception
            self.disable_stream()
            # Handle the exception
            print(f"An error occurred while downloading the file: {str(e)}")
            return None

    async def upload_ftp(self, local_file_path, remote_path, ftp_host, ftp_port=21, ftp_username='', ftp_password='',
                         passive=True):
        """
        Uploads a file to a remote FTP server.

        Parameters:
        - local_file_path (str): The local path of the file to upload.
        - remote_path (str): The remote directory path where the file will be uploaded. If not specified, the file will be uploaded to the root directory.
        - ftp_host (str): The hostname or IP address of the FTP server.
        - ftp_port (int, optional): The port number of the FTP server. Defaults to 21.
        - ftp_username (str, optional): The username for FTP authentication. Defaults to an empty string.
        - ftp_password (str, optional): The password for FTP authentication. Defaults to an empty string.
        - passive (bool, optional): Whether to use passive mode for FTP. Defaults to True.

        Returns:
        - bool: True if the file was successfully uploaded, False otherwise.

        Raises:
        - ConnectionError: If there is an error connecting to the FTP server.
        """

        try:
            if not os.path.exists(local_file_path):
                print(f"The local file '{local_file_path}' does not exist.")
                return False

            with ftplib.FTP() as ftp:
                try:
                    ftp.connect(ftp_host, ftp_port)
                    ftp.login(ftp_username, ftp_password)

                    if passive:
                        ftp.set_pasv(True)
                    else:
                        ftp.set_pasv(False)

                    if remote_path:
                        if remote_path not in ftp.nlst():
                            ftp.mkd(remote_path)
                        ftp.cwd(remote_path)

                    file_name = os.path.basename(local_file_path)
                    if file_name in ftp.nlst():
                        print(f"A file with the name '{file_name}' already exists in the remote directory.")
                        return False

                    file_size = os.path.getsize(local_file_path)

                    with open(local_file_path, 'rb') as file:
                        with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024,
                                  desc=f"Uploading {file_name}", bar_format="{l_bar}{bar}{r_bar}",
                                  colour='green') as pbar:
                            async def callback(data):
                                ftp.storbinary(f'STOR {file_name}', data)
                                pbar.update(len(data))

                            await asyncio.to_thread(callback, file)

                    print(f"The file '{local_file_path}' was successfully uploaded to the FTP server at the remote location '{remote_path}'.")
                    return True

                except ftplib.all_errors as e:
                    print(f"Error uploading file via FTP: {e}")
                    return False
        except ConnectionError:
            print("Error connecting to the FTP server.")
            return False

