from requests_mock import Adapter

from relay_sdk.client import new_session
from relay_sdk.outputs import Outputs


class TestOutputs:

    def test_set(self, requests_mock: Adapter) -> None:
        requests_mock.register_uri(
            'PUT', 'http+api://api/outputs/foo',
            text='OK',
            request_headers={'content-type': 'application/json'},
            additional_matcher=lambda request: request.text == r'"bar"',
        )
        Outputs(new_session(api_url='http://api')).set('foo', 'bar')
