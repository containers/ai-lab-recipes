import validators.url
from urllib.error import URLError, HTTPError
import urllib.request

def download_json_file(url: str, file_name: str):
    if validators.url(url):
        try:
            urllib.request.urlretrieve(url, file_name)
        except HTTPError as e:
            print(f"HTTP Error: {e.code}, {e.reason}")
        except URLError as e:
            print(f"URL Error: {e.reason}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")