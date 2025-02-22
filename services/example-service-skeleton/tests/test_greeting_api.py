# coding: utf-8

from fastapi.testclient import TestClient


from endpoints.models.get_greeting200_response import GetGreeting200Response  # noqa: F401


def test_get_greeting(client: TestClient):
    """Test case for get_greeting

    Returns a greeting and the current time
    """

    headers = {
    }

    response = client.request(
       "GET",
       "/greet",
       headers=headers,
    )

    assert response.status_code == 200
    data: GetGreeting200Response = response.json()
    assert data['message'] == 'Hello World!'

