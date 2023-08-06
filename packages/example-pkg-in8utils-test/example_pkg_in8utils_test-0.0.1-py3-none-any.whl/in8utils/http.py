import requests

from requests import HTTPError, RequestException, ConnectionError
from sentry_sdk import configure_scope

with configure_scope() as scope:
    scope.set_tag("bot", "http_client")


class HttpClientException(Exception):
    """Raises when an error occurs while doing a networking request."""


class GeneralHttpClientException(Exception):
    """Raises when an unexpected error occurs while doing a networking request."""


class HttpClient:
    def __init__(self):
        self.__session = requests.session()
        self.__verb = None
        self.__url = None
        self.__data = None
        self.__json = None
        self.__headers = {}
        self.__proxies = None
        self.__status_code = -1
        self.__message = None
        self.__timeout = 600

    def get(self, url):
        self.__url = url
        self.__verb = "get"
        return self

    def post(self, url):
        self.__url = url
        self.__verb = "post"
        return self

    def data(self, data):
        self.__data = data
        return self

    def json(self, json):
        self.__json = json
        return self

    def header(self, key, value):
        self.__headers[key] = value
        return self

    def headers(self, headers):
        self.__headers = headers
        return self

    def timeout(self, timeout):
        self.__timeout = timeout
        return self

    def proxies(self, proxies):
        self.__proxies = proxies
        return self

    def ensure(self, status_code, message):
        self.__status_code = status_code
        self.__message = message
        return self

    def build(self) -> requests.Response:
        if self.__url is None or self.__url == "":
            raise HttpClientException("URL not provided.")

        if self.__verb not in ["get", "post"]:
            raise HttpClientException("HTTP verb not allowed.")

        if self.__verb == "post" and (self.__data is None and self.__json is None):
            raise HttpClientException("HTTP POST without a payload is not allowed.")

        try:
            if self.__verb == "get":
                response = self.__session.get(
                    url=self.__url,
                    headers=self.__headers,
                    proxies=self.__proxies,
                    timeout=self.__timeout,
                    verify=False)
            else:
                if self.__json is not None:
                    self.header("Content-Type", "application/json; charset=UTF-8")

                response = self.__session.post(
                    url=self.__url,
                    data=self.__data,
                    json=self.__json,
                    headers=self.__headers,
                    proxies=self.__proxies,
                    timeout=self.__timeout,
                    verify=False)

        except HTTPError or RequestException or ConnectionError as _:
            raise HttpClientException("Error while fetching data.", _)
        except Exception as _:
            raise GeneralHttpClientException("Unexpected HTTP Exception", _)

        status_code = response.status_code

        if self.__status_code != -1 and status_code != self.__status_code:
            message = "Request failed, expected status code {}, but received" \
                      " {}.".format(self.__status_code, status_code) \
                if self.__message is not None else self.__message
            raise HttpClientException(message)

        self.__clean()
        return response

    def __clean(self):
        self.__verb = None
        self.__url = None
        self.__data = None
        self.__json = None
        self.__headers = {}
        self.__proxies = None
        self.__status_code = -1
        self.__message = None
        self.__timeout = 600


class HttpClientForTesting:
    def __init__(self):
        self.__session = requests.session()
        self.__verb = None
        self.__url = None
        self.__data = None
        self.__json = None
        self.__headers = {}
        self.__proxies = None
        self.__status_code = -1
        self.__message = None
        self.__timeout = 600

    def get(self, url):
        self.__url = url
        self.__verb = "get"
        return self

    def post(self, url):
        self.__url = url
        self.__verb = "post"
        return self

    def data(self, data):
        self.__data = data
        return self

    def json(self, json):
        self.header("Content-Type", "application/json; charset=UTF-8")
        self.__json = json
        return self

    def header(self, key, value):
        self.__headers[key] = value
        return self

    def headers(self, headers):
        self.__headers = headers
        return self

    def proxies(self, proxies):
        self.__proxies = proxies
        return self

    def ensure(self, status_code, message):
        self.__status_code = status_code
        self.__message = message
        return self

    def timeout(self, timeout):
        self.__timeout = timeout
        return self

    def build(self) -> requests.Response:
        res = Response(self.__headers, self.__data if self.__data else self.__json)
        self.__clean()
        return res

    def __clean(self):
        self.__verb = None
        self.__url = None
        self.__data = None
        self.__json = None
        self.__headers = {}
        self.__proxies = None
        self.__status_code = -1
        self.__message = None
        self.__timeout = 600


class Response(object):
    def __init__(self, headers, data):
        self.headers = headers
        self.content = str(data)
        self.__data = data

    def json(self):
        return self.__data
