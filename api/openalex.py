import requests


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