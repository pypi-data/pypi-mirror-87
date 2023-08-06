import logging
from urllib.parse import urlparse, parse_qs

from .api_client import ApiClient
from .exceptions import ResponseErrorException, ApiKeyNotFoundException


class Resource(object):

    DEFAULT_ITEMS_PER_PAGE = 50

    def __init__(self, api_key=None):
        """
        :param api_key: The API key.
        """
        self._api_client = ApiClient(api_key=api_key)

    def get_page(self, endpoint, params=None, data=None, page=1, per_page=DEFAULT_ITEMS_PER_PAGE):
        """
        Returns all items in a page for the given endpoint.
        :param endpoint: The endpoint.
        :type endpoint: str
        :param params: The list of tuples or bytes to send in the query string for the request.
        :type params: dict, optional
        :param data: The list of tuples, bytes, or file-like object to send in the body of the request.
        :return: :class:`Response <Response>` object
        :param page: The page.
        :type page: int, optional
        :param per_page: The number of items per page.
        :type per_page: int, optional
        :return: The list of items.
        :rtype list
        :raises ResponseErrorException: Whether the response cannot be parsed.
        :raises ApiKeyNotFoundException: Whether the API key is not provider.
        """
        if params is None:
            params = {}
        if data is None:
            data = {}
        params.update({'page': page, 'per-page': per_page})

        return self._api_client.send(method='get', endpoint=endpoint, params=params, data=data)

    def paginate(self, endpoint, params=None, data=None):
        """
        Returns all items for the given endpoint.
        :param endpoint: The endpoint.
        :type endpoint: str
        :param params: The list of tuples or bytes to send in the query string for the request.
        :type params:  dict, optional
        :param data: The list of tuples, bytes, or file-like object to send in the body of the request.
        :return: :class:`Response <Response>` object
        :return: The list of items.
        :rtype list
        """

        if data is None:
            data = {}
        if params is None:
            params = {}

        logging.debug('Sending request to endpoint %s...' % endpoint)
        has_next = True
        page = 1
        while has_next:
            logging.debug('Processing page %d...' % page)
            response = self.get_page(endpoint=endpoint, params=params, data=data, page=page)
            logging.debug('Found %d results...' % len(response.json()))

            for entry in response.json():
                yield entry

            if 'next' in response.links:
                parsed = urlparse(response.links['next']['url'])
                page = int(parse_qs(parsed.query)['page'][0])
            else:
                has_next = False
