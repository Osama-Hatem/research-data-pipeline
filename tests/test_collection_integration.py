from database.connection import get_connection
from database.schema import create_tables
from database.reader import (
    search_papers,
    get_authors_for_paper
)
from collection.service import process_papers


def test_collection_pipeline_saves_paper_and_author():

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    raw_papers = [

        {

            "id": "https://openalex.org/W123",

            "title": "Machine Learning Research",

            "publication_date": "2025-01-01",

            "cited_by_count": 42,

            "doi": "https://doi.org/example",

            "primary_location": {

                "landing_page_url":
                "https://example.com"

            },

            "authorships": [

                {

                    "author": {

                        "id":
                        "https://openalex.org/A123",

                        "display_name":
                        "Ada Lovelace"

                    }

                }

            ]

        }

    ]


    result = process_papers(
        raw_papers,
        "machine learning",
        connection
    )


    assert result[
        0
    ] == 1


    assert result[
        1
    ] == 0


    assert result[
        2
    ] == 0


    papers = search_papers(
        connection,
        "Machine Learning Research",
        10,
        "citations"
    )


    assert len(
        papers
    ) == 1


    paper = papers[0]


    assert paper[2] == (
        "Machine Learning Research"
    )


    authors = get_authors_for_paper(
        connection,
        paper[0]
    )


    assert len(
        authors
    ) == 1


    assert authors[0][0] == (
        "Ada Lovelace"
    )


    connection.close()