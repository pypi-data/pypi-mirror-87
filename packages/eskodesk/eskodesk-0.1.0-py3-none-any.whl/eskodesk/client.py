import logging
from typing import Dict, Iterable, Optional

import requests
from requests import Response

from eskodesk import exceptions

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 15


class Eskodesk:
    def __init__(self, token=None, base_url=None, timeout=DEFAULT_TIMEOUT):
        self._token = token
        self._base_url = base_url
        self._timeout = timeout
        self._user_agent = "eskodesk-python-client"

    def _build_url(self, endpoint: str) -> str:
        return f"{self._base_url}/api/{endpoint}/"

    def _request(self, method: str, url: str, params: Optional[Dict] = None, json: Optional[Dict] = None) -> Response:
        headers = {"Authorization": f"Token {self._token}", "User-Agent": self._user_agent}

        try:
            response = requests.request(
                method=method, url=url, params=params, json=json, headers=headers, timeout=self._timeout
            )

            status = response.status_code

            if status >= 400 and status < 500:
                if status == 400:
                    raise exceptions.EskodeskBadRequest(response.text)
                elif status == 401:
                    logger.critical("Tried to consume the Eskodesk API with bad credentials.")
                    raise exceptions.EskodeskBadCredentials(response.text)
                elif status == 404:
                    raise exceptions.EskodeskObjectNotFound(response.text)
                else:
                    raise exceptions.EskodeskClientError(response.text)

            elif status >= 500:
                logger.critical(f"Eskodesk API returned a server error response ({status}) for the endpoint {url}.")
                raise exceptions.EskodeskServerError(response.text)

            return response
        except requests.exceptions.Timeout:
            # Safe to retry the same call.
            logger.exception("The Eskodesk API took too long to respond.")
            raise exceptions.EskodeskConnectTimeout(
                "The Eskodesk API didn't respond in a timely manner. Try again later."
            )
        except requests.exceptions.RequestException:
            logger.exception(f"A request error occurred while trying to consume the endpoint {url}.")
            raise exceptions.EskodeskException("An unexpected error occurred.")

    def _request_endpoint(
        self, method: str, endpoint: str, params: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> Dict:
        url = self._build_url(endpoint)
        response = self._request(method=method, url=url, params=params, json=json)
        if response.status_code == 204:
            return {}
        return response.json()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        return self._request_endpoint(method="get", endpoint=endpoint, params=params)

    def _get_paginated_results(self, endpoint: str, params: Optional[Dict] = None) -> Iterable[Dict]:
        data = self._get(endpoint, params=params)
        while True:
            for page in data["results"]:
                yield page
            if data["next"] is not None:
                response = self._request(method="get", url=data["next"])
                data = response.json()
            else:
                break

    def _post(self, endpoint: str, json: Optional[Dict] = None) -> Dict:
        return self._request_endpoint(method="post", endpoint=endpoint, json=json)

    def _patch(self, endpoint: str, json: Optional[Dict] = None) -> Dict:
        return self._request_endpoint(method="patch", endpoint=endpoint, json=json)

    def _delete(self, endpoint: str, json: Optional[Dict] = None) -> Dict:
        return self._request_endpoint(method="delete", endpoint=endpoint, json=json)

    def create_ticket(self, json: Dict):
        return self._post("tickets", json=json)
