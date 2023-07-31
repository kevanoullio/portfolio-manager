# Purpose: Web Scraper module for making web requests and parsing HTML tables.

# Standard Libraries
import requests

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# WebScraper class for making web requests and parsing HTML tables
class WebScraper:
    def __init__(self, user_agent: bool) -> None:
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"} if user_agent else {}
        self.session = requests.Session()

    def _make_get_request(self, url: str) -> requests.Response:
        response = self.session.get(url, headers=self.headers)
        return response

    def _get_response_text(self, response: requests.Response) -> str:
        return response.text

    def _get_response_content(self, response: requests.Response) -> bytes:
        return response.content

    def get_html_content_as_text(self, url: str) -> str | None:
        response = self._make_get_request(url)
        if response.status_code == 200:
            html_content = self._get_response_text(response)
            return html_content
        else:
            print(f"Request failed with status code: {response.status_code}")
            logging.info(f"Request failed with status code: {response.status_code}")
            return None
        
    def get_html_content_as_bytes(self, url: str) -> bytes | None:
        response = self._make_get_request(url)
        if response.status_code == 200:
            html_content = self._get_response_content(response)
            return html_content
        else:
            print(f"Request failed with status code: {response.status_code}")
            logging.info(f"Request failed with status code: {response.status_code}")
            return None


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
