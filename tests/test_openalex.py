import requests

from api.openalex import get_papers


def test_get_papers_returns_results(
    monkeypatch
):

    class FakeResponse:

        def raise_for_status(
            self
        ):

            pass


        def json(
            self
        ):

            return {

                "results": [

                    {
                        "id": "W123"
                    }

                ]

            }


    def fake_get(
        *args,
        **kwargs
    ):

        return FakeResponse()


    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )


    result = get_papers(
        "engineering"
    )


    assert result == [

        {
            "id": "W123"
        }

    ]


def test_get_papers_does_not_retry_bad_request(
    monkeypatch
):

    attempts = []


    class FakeResponse:

        def raise_for_status(
            self
        ):

            response = requests.Response()

            response.status_code = 400


            raise requests.HTTPError(
                response=response
            )


    def fake_get(
        *args,
        **kwargs
    ):

        attempts.append(
            1
        )


        return FakeResponse()


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


    else:

        raise AssertionError(
            "Expected HTTPError"
        )


    assert len(attempts) == 1


def test_get_papers_retries_server_error(
    monkeypatch
):

    attempts = []


    class FakeResponse:

        def raise_for_status(
            self
        ):

            response = requests.Response()

            response.status_code = 500


            raise requests.HTTPError(
                response=response
            )


    def fake_get(
        *args,
        **kwargs
    ):

        attempts.append(
            1
        )


        return FakeResponse()


    def fake_sleep(
        delay
    ):

        pass


    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )


    monkeypatch.setattr(
        "api.openalex.time.sleep",
        fake_sleep
    )


    try:

        get_papers(
            "engineering"
        )


    except requests.HTTPError:

        pass


    else:

        raise AssertionError(
            "Expected HTTPError"
        )


    assert len(attempts) == 3


def test_get_papers_retries_timeout(
    monkeypatch
):

    attempts = []


    def fake_get(
        *args,
        **kwargs
    ):

        attempts.append(
            1
        )


        raise requests.Timeout()


    def fake_sleep(
        delay
    ):

        pass


    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )


    monkeypatch.setattr(
        "api.openalex.time.sleep",
        fake_sleep
    )


    try:

        get_papers(
            "engineering"
        )


    except requests.Timeout:

        pass


    else:

        raise AssertionError(
            "Expected Timeout"
        )


    assert len(attempts) == 3


def test_get_papers_retries_connection_error(
    monkeypatch
):

    attempts = []


    def fake_get(
        *args,
        **kwargs
    ):

        attempts.append(
            1
        )


        raise requests.ConnectionError()


    def fake_sleep(
        delay
    ):

        pass


    monkeypatch.setattr(
        requests,
        "get",
        fake_get
    )


    monkeypatch.setattr(
        "api.openalex.time.sleep",
        fake_sleep
    )


    try:

        get_papers(
            "engineering"
        )


    except requests.ConnectionError:

        pass


    else:

        raise AssertionError(
            "Expected ConnectionError"
        )


    assert len(attempts) == 3