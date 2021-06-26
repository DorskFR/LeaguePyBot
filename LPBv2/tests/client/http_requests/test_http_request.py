from LPBv2.client import HTTPRequest, HTTPConnection
from LPBv2.common import ClientResponse
import pytest


@pytest.fixture
def http_request():
    return HTTPRequest()


def test_http_request_init(http_request):
    assert isinstance(http_request.http, HTTPConnection)


@pytest.mark.asyncio
async def test_http_request_request(http_request):
    response = await http_request.request(method="POST", endpoint="/Help")
    assert response
    assert isinstance(response, ClientResponse)
