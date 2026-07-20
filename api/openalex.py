import time

import requests

from config.settings import (
    OPENALEX_API_URL,
    OPENALEX_TIMEOUT,
    OPENALEX_PER_PAGE,
    OPENALEX_MAX_RETRIES,
    OPENALEX_RETRY_DELAY
)


def get_papers(
    search_term
):

    for attempt in range(
        OPENALEX_MAX_RETRIES
    ):

        try:

            response = requests.get(
                OPENALEX_API_URL,
                params={
                    "search": search_term,
                    "per-page": (
                        OPENALEX_PER_PAGE
                    )
                },
                timeout=OPENALEX_TIMEOUT
            )


            response.raise_for_status()


            data = response.json()


            return data["results"]


        except requests.HTTPError as error:

            status_code = (
                error.response.status_code
            )


            if status_code < 500:

                raise


            if (
                attempt
                == OPENALEX_MAX_RETRIES - 1
            ):

                raise


            time.sleep(
                OPENALEX_RETRY_DELAY
            )


        except (
            requests.ConnectionError,
            requests.Timeout
        ):

            if (
                attempt
                == OPENALEX_MAX_RETRIES - 1
            ):

                raise


            time.sleep(
                OPENALEX_RETRY_DELAY
            )