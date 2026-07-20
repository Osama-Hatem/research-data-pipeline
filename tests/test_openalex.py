import requests
from api.openalex import get_papers
from database.connection import get_connection
from database.schema import create_tables
from database.reader import (
    get_database_statistics
)
from database.repository import save_paper
from database.reader import get_recent_papers, get_papers_for_author, search_authors, get_top_cited_papers

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

def test_get_database_statistics():

    connection = get_connection(
        ":memory:"
    )

    create_tables(
        connection
    )

    statistics = get_database_statistics(
        connection
    )

    assert statistics["papers"] == 0

    assert statistics["authors"] == 0

    assert statistics["relationships"] == 0

    assert statistics["average_citations"] == 0

    connection.close()

def test_get_recent_papers():

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    paper_one = {

        "openalex_id": "W1",

        "title": "Older Paper",

        "publication_date": "2025-01-01",

        "citations": 10,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []

    }


    paper_two = {

        "openalex_id": "W2",

        "title": "Newer Paper",

        "publication_date": "2026-01-01",

        "citations": 20,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []

    }


    save_paper(
        paper_one,
        connection
    )


    save_paper(
        paper_two,
        connection
    )


    recent = get_recent_papers(
        connection,
        2
    )


    assert len(
        recent
    ) == 2


    connection.close()

def test_search_authors():

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    connection.execute(
        """
        INSERT INTO authors (
            openalex_id,
            name
        )
        VALUES (?, ?)
        """,
        (
            "A123",
            "Ada Lovelace"
        )
    )


    connection.commit()


    authors = search_authors(
        connection,
        "Ada",
        10
    )


    assert len(
        authors
    ) == 1


    assert authors[0][2] == (
        "Ada Lovelace"
    )


    connection.close()

def test_get_papers_for_author():

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    paper = {

        "openalex_id": "W123",

        "title": "Research Paper",

        "publication_date": "2025-01-01",

        "citations": 42,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": [

            {

                "openalex_id": "A123",

                "name": "Ada Lovelace",

                "position": 0

            }

        ]

    }


    save_paper(
        paper,
        connection
    )


    author = connection.execute(
        """
        SELECT id
        FROM authors
        WHERE openalex_id = ?
        """,
        (
            "A123",
        )
    ).fetchone()


    papers = get_papers_for_author(
        connection,
        author[0]
    )


    assert len(
        papers
    ) == 1


    assert papers[0][2] == (
        "Research Paper"
    )


    connection.close()

def test_get_top_cited_papers():

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    papers = [

        {

            "openalex_id": "W1",

            "title": "Low Citation Paper",

            "publication_date": "2025-01-01",

            "citations": 10,

            "doi": None,

            "primary_url": None,

            "search_query": "engineering",

            "authors": []

        },

        {

            "openalex_id": "W2",

            "title": "High Citation Paper",

            "publication_date": "2025-01-01",

            "citations": 100,

            "doi": None,

            "primary_url": None,

            "search_query": "engineering",

            "authors": []

        },

        {

            "openalex_id": "W3",

            "title": "Medium Citation Paper",

            "publication_date": "2025-01-01",

            "citations": 50,

            "doi": None,

            "primary_url": None,

            "search_query": "engineering",

            "authors": []

        }

    ]


    for paper in papers:

        save_paper(
            paper,
            connection
        )


    result = get_top_cited_papers(
        connection,
        3
    )


    assert len(
        result
    ) == 3


    assert result[0][2] == (
        "High Citation Paper"
    )


    assert result[1][2] == (
        "Medium Citation Paper"
    )


    assert result[2][2] == (
        "Low Citation Paper"
    )


    connection.close()