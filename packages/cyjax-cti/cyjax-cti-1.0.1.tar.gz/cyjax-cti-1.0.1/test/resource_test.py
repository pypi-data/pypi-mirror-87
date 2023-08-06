#  CYjAX Limited

import responses

from cyjax.api_client import ApiClient
from cyjax.resource import Resource


class TestResourceService:

    @responses.activate
    def test_paginate(self):

        responses.add(responses.GET, ApiClient.BASE_URI + '/test/endpoint?param1=test&param2=foo&page=1&per-page='
                      + str(Resource.DEFAULT_ITEMS_PER_PAGE),
                      json=[{"1": "a"}, {"2": "b"}], status=200,
                      headers={'Link': ApiClient.BASE_URI +
                                       '/test/endpoint?param1=test&param2=foo&page=2&per-page=1;rel=next'})

        responses.add(responses.GET, ApiClient.BASE_URI + '/test/endpoint?param1=test&param2=foo&page=2&per-page='
                      + str(Resource.DEFAULT_ITEMS_PER_PAGE),
                      json=[{"3": "c"}, {"4": "d"}], status=200)

        resource_service = Resource(api_key='9753b80f76bd4293e8c610b07091a37b')
        for x in resource_service.paginate(endpoint='test/endpoint', params={'param1': 'test', 'param2': 'foo'}):
            continue

        assert len(responses.calls) == 2
        assert responses.calls[0].request.url == ApiClient.BASE_URI + \
               '/test/endpoint?param1=test&param2=foo&page=1&per-page=' + str(Resource.DEFAULT_ITEMS_PER_PAGE)
        assert responses.calls[0].response.text == '[{"1": "a"}, {"2": "b"}]'

        assert responses.calls[1].request.url == ApiClient.BASE_URI + \
               '/test/endpoint?param1=test&param2=foo&page=2&per-page=' + str(Resource.DEFAULT_ITEMS_PER_PAGE)
        assert responses.calls[1].response.text == '[{"3": "c"}, {"4": "d"}]'
