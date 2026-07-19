import requests

import pytest

from api.openalex import get_papers


def test_get_papers_retries_after_timeout(
    monkeypatch
):

    attempts = 0


    def fake_get(
        *args,
        **kwargs
    ):

        nonlocal attempts

        attempts += 1


        if attempts < 3:

            raise requests.Timeout()


        class FakeResponse:

            def raise_for_status(self):

                pass


            def json(self):

                return {
                    "results": []
                }


        return FakeResponse()


    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )


    result = get_papers(
        "engineering"
    )


    assert result == []

    assert attempts == 3


def test_get_papers_does_not_retry_bad_request(
    monkeypatch
):

    attempts = 0


    def fake_get(
        *args,
        **kwargs
    ):

        nonlocal attempts

        attempts += 1


        response = requests.Response()


        response.status_code = 400


        response.url = (
            "https://api.openalex.org/works"
        )


        return response


    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )


    try:

        get_papers(
            "engineering"
        )

    except requests.HTTPError:

        pass


    assert attempts == 1