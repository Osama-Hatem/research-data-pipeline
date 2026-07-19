import requests

from tenacity import retry
from tenacity import retry_if_exception
from tenacity import stop_after_attempt
from tenacity import wait_exponential


def should_retry(error):

    if isinstance(
        error,
        requests.Timeout
    ):

        return True


    if isinstance(
        error,
        requests.ConnectionError
    ):

        return True


    if isinstance(
        error,
        requests.HTTPError
    ):

        status_code = (
            error.response.status_code
        )


        return status_code in {
            429,
            500,
            502,
            503,
            504
        }


    return False


@retry(
    retry=retry_if_exception(
        should_retry
    ),
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=1,
        max=10
    )
)
def get_papers(search_term):

    response = requests.get(
        "https://api.openalex.org/works",
        params={
            "search": search_term,
            "per-page": 25
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["results"]