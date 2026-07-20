import pytest
from database.reader import search_papers
from database.connection import get_connection
from database.schema import create_tables
from database.repository import save_paper
from reader import search_papers


def test_search_papers_finds_paper_by_title():

    connection = get_connection(
        ":memory:"
    )

    create_tables(
        connection
    )


    paper = {

        "openalex_id": "W-SEARCH-1",

        "title": "Introduction to Engineering",

        "publication_date": "2025-01-01",

        "citations": 100,

        "doi": None,

        "primary_url": None,

        "search_query": "science",

        "authors": []

        }


    save_paper(
        paper,
        connection
    )


    results = search_papers(
        connection,
        "Engineering"
    )


    assert len(results) == 1

    assert results[0][2] == (
        "Introduction to Engineering"
    )


    connection.close()

def test_search_papers_finds_paper_by_author():

    connection = get_connection(
        ":memory:"
    )

    create_tables(
        connection
    )


    paper = {

        "openalex_id": "W-SEARCH-2",

        "title": "A Research Paper",

        "publication_date": "2025-01-01",

        "citations": 50,

        "doi": None,

        "primary_url": None,

        "search_query": "science",

        "authors": [

            {

                "openalex_id": "A-SEARCH-1",

                "name": "Ada Lovelace",

                "position": 0

            }

        ]

    }


    save_paper(
        paper,
        connection
    )


    results = search_papers(
        connection,
        "Ada Lovelace"
    )


    assert len(results) == 1

    assert results[0][2] == (
        "A Research Paper"
    )


    connection.close()

def test_search_papers_returns_most_cited_first():

    connection = get_connection(
        ":memory:"
    )

    create_tables(
        connection
    )


    low_citation_paper = {

        "openalex_id": "W-LOW",

        "title": "Engineering Basics",

        "publication_date": "2025-01-01",

        "citations": 10,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []

    }


    high_citation_paper = {

        "openalex_id": "W-HIGH",

        "title": "Advanced Engineering",

        "publication_date": "2025-01-01",

        "citations": 500,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []

    }


    save_paper(
        low_citation_paper,
        connection
    )


    save_paper(
        high_citation_paper,
        connection
    )


    results = search_papers(
        connection,
        "engineering"
    )


    assert len(results) == 2


    assert results[0][2] == (
        "Advanced Engineering"
    )


    assert results[1][2] == (
        "Engineering Basics"
    )


    connection.close()

def test_search_papers_respects_limit():

    connection = get_connection(
        ":memory:"
    )

    create_tables(
        connection
    )


    for number in range(5):

        paper = {

            "openalex_id": (
                f"W-LIMIT-{number}"
            ),

            "title": (
                f"Engineering Paper {number}"
            ),

            "publication_date": (
                "2025-01-01"
            ),

            "citations": number,

            "doi": None,

            "primary_url": None,

            "search_query": (
                "engineering"
            ),

            "authors": []

        }


        save_paper(
            paper,
            connection
        )


    results = search_papers(
        connection,
        "engineering",
        limit=2
    )


    assert len(results) == 2


    connection.close()

def test_search_papers_can_sort_by_title():

    connection = get_connection(
        ":memory:"
    )

    create_tables(
        connection
    )


    for title in [

        "Zebra Engineering",

        "Alpha Engineering"

    ]:

        paper = {

            "openalex_id": title,

            "title": title,

            "publication_date": (
                "2025-01-01"
            ),

            "citations": 10,

            "doi": None,

            "primary_url": None,

            "search_query": (
                "engineering"
            ),

            "authors": []

        }


        save_paper(
            paper,
            connection
        )


    results = search_papers(
        connection,
        "engineering",
        sort_by="title"
    )


    assert results[0][2] == (
        "Alpha Engineering"
    )


    assert results[1][2] == (
        "Zebra Engineering"
    )


    connection.close()

def test_search_papers_rejects_invalid_sort():

    connection = get_connection(
        ":memory:"
    )

    try:

        create_tables(
            connection
        )


        try:

            search_papers(
                connection,
                "engineering",
                sort_by="invalid"
            )


        except ValueError:

            pass


        else:

            pytest.fail(
                "Expected ValueError"
            )


    finally:

        connection.close()