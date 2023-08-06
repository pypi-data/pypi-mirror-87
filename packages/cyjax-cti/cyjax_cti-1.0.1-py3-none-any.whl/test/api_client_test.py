import pytest
import responses

import cyjax
from cyjax import ResponseErrorException, ApiKeyNotFoundException
from cyjax.api_client import ApiClient
from cyjax.exceptions import UnauthorizedException


class TestApiClient:

    def test_api_key_is_not_set(self):
        api_client = ApiClient()
        with pytest.raises(ApiKeyNotFoundException) as exception:
            api_client.send(method='get', endpoint='test/endpoint')

    def test_set_api_key_on_module(self):
        cyjax.api_key = 'module_api_key'
        api_client = ApiClient()
        assert api_client.get_api_key() == 'module_api_key'

    def test_set_api_key_on_constructor(self):
        api_client = ApiClient(api_key='constructor_api_key')
        assert api_client.get_api_key() == 'constructor_api_key'

    def test_set_api_key_on_constructor_has_preferences_over_module(self):
        cyjax.api_key = 'module_api_key'
        api_client = ApiClient(api_key='constructor_api_key')
        assert api_client.get_api_key() == 'constructor_api_key'

    @responses.activate
    def test_send(self,):
        responses.add(responses.GET, ApiClient.BASE_URI + '/test/endpoint?param1=test&param2=foo',
                      json=[{'1': 'a', '2': 'b', '3': [1, 2, 3]}], status=200)

        api_client = ApiClient(api_key='foo_api_key')
        response = api_client.send(method='get', endpoint='test/endpoint', params={'param1': 'test', 'param2': 'foo'},
                                   data={'foo': 'test'})

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == ApiClient.BASE_URI + '/test/endpoint?param1=test&param2=foo'
        assert responses.calls[0].request.body == "foo=test"
        assert responses.calls[0].response.text == '[{"1": "a", "2": "b", "3": [1, 2, 3]}]'

        assert response.status_code == 200
        assert response.json() == [{'1': 'a', '2': 'b', '3': [1, 2, 3]}]

    @responses.activate
    def test_rest_request_throw_exception(self):
        responses.add(responses.GET, ApiClient.BASE_URI + '/test/endpoint',
                      json={'name': 'Unauthorized', 'message': 'The access token provided is invalid'},
                      status=401)

        api_client = ApiClient(api_key='foo_api_key')
        with pytest.raises(UnauthorizedException):
            api_client.send(method='get', endpoint='test/endpoint')
