from json.decoder import JSONDecodeError

import requests

import cyjax
from .exceptions import ResponseErrorException, ApiKeyNotFoundException, UnauthorizedException, TooManyRequestsException


class ApiClient(object):

    """
    The Cyjax REST API URL.
    """
    BASE_URI = 'https://api.cyberportal.co'

    def __init__(self, api_key=None):
        """
        :param api_key: The API key.
        """
        self.__api_key = api_key if api_key else cyjax.api_key

    def send(self, method, endpoint, params=None, data=None):
        """
        Send a request to an endpoint.
        :param method: The request method: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``
        :type method: str
        :param endpoint: The endpoint.
        :type endpoint: str
        :param params: The list of tuples or bytes to send in the query string for the request
        :type params:  Dictionary, optional
        :param data: The list of tuples, bytes, or file-like object to send in the body of the request
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        :raises ResponseErrorException: Whether the request fails.
        :raises ApiKeyNotFoundException: Whether the API key is not provided.
        :raises UnauthorizedException: Whether the API key is not authorized to perform the request.
        :raises TooManyRequestsException: Whether the API key exceeds the rate limit.
        """

        if data is None:
            data = {}
        if params is None:
            params = {}
        if not self.__api_key:
            raise ApiKeyNotFoundException()

        response = requests.api.request(method=method, url=self.BASE_URI + '/' + endpoint, params=params,
                                        data=data, headers={'Authorization': 'Bearer ' + self.__api_key})

        if response.status_code == 401:
            raise UnauthorizedException()
        elif response.status_code == 429:
            raise TooManyRequestsException()
        elif response.status_code != 200:
            try:
                json_data = response.json()
                raise ResponseErrorException(response.status_code, json_data['message'] if 'message' in json_data else 'Unknown')
            except JSONDecodeError:
                raise ResponseErrorException(response.status_code, 'Error parsing response %s' % response.text)

        return response

    def get_api_key(self):
        """
        Get API key.
        :return: The API key.
        :rtype: str
        """
        return self.__api_key
