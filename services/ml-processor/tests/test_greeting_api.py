# coding: utf-8

from fastapi.testclient import TestClient


from endpoints.models.get_greeting200_response import GetGreeting200Response  # noqa: F401


def test_get_greeting(client: TestClient):
    """Test case for get_greeting

    Returns a greeting and the current time
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ml-processor/ping",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

