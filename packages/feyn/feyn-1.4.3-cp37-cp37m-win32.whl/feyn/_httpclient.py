"""
HttpClient based on requests, that takes care of setting up:
- The base url for the API
- Default headers
- And a retry policy

The returned client, has same interface as the requests module.
"""
from http import HTTPStatus

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient(requests.Session):
    def __init__(self, api_base_url, default_headers={}):
        super(HttpClient, self).__init__()

        retry_policy = self._get_retry_policy()
        adapter = HTTPAdapter(max_retries=retry_policy)
        self.mount('http://', adapter)
        self.mount('https://', adapter)

        self.headers.update(default_headers)
        self.api_base_url = api_base_url

        if self.api_base_url.endswith("/"):
            raise ValueError("Dont end the api_base_url with a '/' please.")

    def request(self, method, url, *args, **kwargs):
        if not url.startswith("/"):
            raise ValueError("Start with a '/' please.")

        # Hack to be able to access the qlattice information on 'http:/.../api/v1/qlattice'.
        # Public facing api paths should be revisited to remove this hack.
        if url == "/":
            url = ""

        url = self.api_base_url + url
        return super(HttpClient, self).request(method, url, *args, **kwargs)

    def _get_retry_policy(self):
        return Retry(
            total=2,
            backoff_factor=2,
            raise_on_status=False,
            method_whitelist=['GET', 'PUT', 'POST', 'DELETE'],
            status_forcelist=[
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.GATEWAY_TIMEOUT
            ],
        )
