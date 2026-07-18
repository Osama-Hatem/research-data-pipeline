from database.connection import get_connection
from database.schema import create_tables
from database.repository import save_paper


def test_save_paper():

    connection = get_connection(":memory:")

    create_tables(connection)


    paper = {

        "openalex_id": "W123",

        "title": "A Research Paper",

        "publication_date": "2025-01-01",

        "citations": 42,

        "doi": "https://doi.org/example",

        "primary_url": "https://example.com",

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


    saved_paper = connection.execute(
        """
        SELECT *
        FROM papers
        WHERE openalex_id = ?
        """,
        ("W123",)
    ).fetchone()


    assert saved_paper is not None

    assert saved_paper[2] == "A Research Paper"


    saved_author = connection.execute(
        """
        SELECT *
        FROM authors
        WHERE openalex_id = ?
        """,
        ("A123",)
    ).fetchone()


    assert saved_author is not None

    assert saved_author[2] == "Ada Lovelace"


    relationship = connection.execute(
        """
        SELECT *
        FROM paper_authors
        """
    ).fetchone()


    assert relationship is not None

    assert relationship[2] == 0


    connection.close()

def test_duplicate_paper_is_not_inserted_twice():

    connection = get_connection(":memory:")

    create_tables(connection)


    paper = {

        "openalex_id": "W123",

        "title": "A Research Paper",

        "publication_date": "2025-01-01",

        "citations": 42,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []
    }


    save_paper(
        paper,
        connection
    )


    save_paper(
        paper,
        connection
    )


    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM papers
        WHERE openalex_id = ?
        """,
        ("W123",)
    ).fetchone()[0]


    assert count == 1


    connection.close()