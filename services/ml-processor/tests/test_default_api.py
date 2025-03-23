# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictStr  # noqa: F401


def test_ping_get(client: TestClient):
    """Test case for ping_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ping",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

