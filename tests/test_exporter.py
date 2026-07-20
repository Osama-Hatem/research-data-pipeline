from database.connection import get_connection
from database.schema import create_tables
from database.repository import save_paper
from database.exporter import (
    export_papers_to_csv,
    export_papers_to_json
)


def create_test_paper():

    return {

        "openalex_id": "W123",

        "title": "Research Paper",

        "publication_date": "2025-01-01",

        "citations": 42,

        "doi": None,

        "primary_url": None,

        "search_query": "engineering",

        "authors": []

    }


def test_export_papers_to_csv(
    tmp_path
):

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    save_paper(
        create_test_paper(),
        connection
    )


    output_file = (
        tmp_path
        / "papers.csv"
    )


    export_papers_to_csv(
        connection,
        output_file
    )


    assert output_file.exists()


    content = (
        output_file
        .read_text(
            encoding="utf-8"
        )
    )


    assert (
        "Research Paper"
        in content
    )


    connection.close()

def test_export_papers_to_json(
    tmp_path
):

    connection = get_connection(
        ":memory:"
    )


    create_tables(
        connection
    )


    save_paper(
        create_test_paper(),
        connection
    )


    output_file = (
        tmp_path
        / "papers.json"
    )


    export_papers_to_json(
        connection,
        output_file
    )


    assert output_file.exists()


    content = (
        output_file
        .read_text(
            encoding="utf-8"
        )
    )


    assert (
        "Research Paper"
        in content
    )


    connection.close()